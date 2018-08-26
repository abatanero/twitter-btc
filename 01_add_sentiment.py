import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import os

# location of tweets
outputFolder = "downloadedTweets/"

# create object for sentiment detection
try:
    sid = SentimentIntensityAnalyzer()
except:
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()

def getSentiment(x):
    s = sid.polarity_scores(x)
    neg = s['neg']
    pos = s['pos']
    neu = s['neu']
    if neg > pos and neg > neu:
        return 'negative'
    elif pos > neg and pos > neu:
        return 'positive'
    else:
        return 'neutral'

for f in os.listdir(outputFolder):
    df = pd.read_csv(outputFolder + f)
    df['sentiment'] = df.text.apply(getSentiment)
    df.to_csv(outputFolder + f, index=False)
