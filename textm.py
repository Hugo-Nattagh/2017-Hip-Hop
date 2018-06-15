import pandas as pd
import os
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

pd.options.display.max_colwidth = 17

analyzer = SentimentIntensityAnalyzer()


def s_analysis(file_df):
    lyrics = pd.DataFrame(data=file_df)
    album = lyrics['songs'][0]['album']
    artist = lyrics['artist'][0]
    lyrics['title'] = lyrics['songs'][0]['title']

    n = 0

    while n < len(lyrics):
        lyrics['title'][n] = lyrics['songs'][n]['title']
        lyrics['songs'][n] = lyrics['songs'][n]['lyrics'].replace('\n', ' ')
        n += 1

    # pprint(lyrics)

    # 1) Basic Feature Extraction

    stop = stopwords.words('english')
    lyrics['stopwords'] = lyrics['songs'].apply(lambda x: len([x for x in x.split() if x in stop]))

    # 2) Basic Pre-Processing

    lyrics['songs'] = lyrics['songs'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    lyrics['songs'] = lyrics['songs'].str.replace('[^\w\s]', '')
    lyrics['songs'] = lyrics['songs'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    TextBlob(lyrics['songs'][0]).words
    lyrics['songs'] = lyrics['songs'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    lyrics['sentimentTxtB'] = lyrics['songs'].apply(lambda x: TextBlob(x).sentiment[0])
    lyrics['sentimentTxtB'] = lyrics['sentimentTxtB'].round(3)
    # lyrics = lyrics.sort_values('sentimentTxtB', ascending=False)

    lyrics['sentimentVaderPos'] = lyrics['songs'].apply(lambda x: analyzer.polarity_scores(x)['pos'])
    lyrics['sentimentVaderNeg'] = lyrics['songs'].apply(lambda x: analyzer.polarity_scores(x)['neg'])

    lyrics['Vader'] = lyrics['sentimentVaderPos'] - lyrics['sentimentVaderNeg']

    nb_rows = len(lyrics.index)
    total_sent = sum(lyrics['sentimentTxtB'])
    avg = total_sent / nb_rows

    total_vad = sum(lyrics['Vader'])
    avg_vad = total_vad / nb_rows

    print(lyrics[['title', 'songs', 'sentimentTxtB', 'Vader']])
    avg = round(avg, 3)
    avg_vad = round(avg_vad, 3)
    print(album + ' by ' + artist + ' - TextBlob: ' + str(avg) + ", Vader: " + str(avg_vad))
    return album, artist, avg, avg_vad


index = len([filename for filename in os.listdir(os.getcwd()) if filename.endswith(".json")])
varb = 0
avg_df = pd.DataFrame(index=range(index), columns=['album', 'artist', 'sent_avg_txtB', 'sent_avg_vad'])

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".json"):
        df = pd.read_json(filename)
        avg_df['album'][varb], avg_df['artist'][varb], avg_df['sent_avg_txtB'][varb], avg_df['sent_avg_vad'][varb] = s_analysis(df)
        varb += 1
        continue
    else:
        continue

avg_df['final_average'] = (avg_df['sent_avg_txtB'] + avg_df['sent_avg_vad']) / 2

avg_df = avg_df.sort_values(by=['final_average'], ascending=False)
print(avg_df)
