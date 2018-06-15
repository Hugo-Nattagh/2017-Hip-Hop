# 2017Hip-Hop

### 2017 Rap Albums’ Text Mining and Sentiment Analysis

A lot of rappers claim to deliver a positive message to the world, which can often be challenging to believe when listening to the lyrics.

How about putting some albums to the test with sentiment analysis?

Sentiment analysis is a natural language processing technique used on texts to detect the overall opinion of the author (negative, neutral or positive).

#### The Data

I knew [Genius.com](https://genius.com/) had to be one of the best databases for this, where the lyrics are transcripted by its community.

To get the lyrics, I used [lyricsGenius](https://github.com/johnwmillr/LyricsGenius), a Python library by [Johnwmillr](https://github.com/johnwmillr)

It’s very useful but unfortunately cannot get all the lyrics for an album, I had to do a query for each song.

I forked his repo and tried my hand at improving his script but realized that his library is using Genius.com’s API, which only allows requests for artists and songs.

So I worked around it in a way that doesnt make my modifications fit with his library.  

I used Beautiful Soup to scrape the songs’ titles from the album page, and made a loop to request all those songs with lyricsGenius.

#### What's going on

I wrote a script to process the lyrics of each songs to optimize the sentiment analysis.

I used TextBlob and Vader for the sentiment analysis of each song of an album, then calculated the average for each album.

The results I got were not what I was hoping for, but made sense. Sentiment analysis is usually used for tweets or reviews, and not for a song’s lyrics. Especially rap, which often contains a lot of slang, wordplays, double entendres... Also a song’s length gives a lot more neutral expressions which leads the average to be close to zero.

Long story short, sentiment analysis, as for now, isn’t the way to go to measure an album’s positiveness.

I visualized it anyway, to see the relative ranking with this technique.

![alt text](https://github.com/Hugo-Nattagh/2017-Hip-Hop/blob/master/Ranking.png)

By doing this project, I warmed up with text mining and sentiment analysis on python, and I’d like to go on with another year, or all verses from an artist, or his discography... But I would need to get a closer look at the existing dictionnaries to, if possible, somehow adjust them to rap lyrics. Or maybe remove all expressions that are too neutral.

#### Files Description

- `api.py`: Script to get the albums' lyrics in json files
- `textm.py`: Script to perform sentiment analysis on the json files
- `Ranking.png`: Visualization of my results
- `requirements.txt`: What you need in order to make it work
