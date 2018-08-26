#!/usr/bin/env python
# encoding: utf-8

#import datetime
import tweet_easy.tweet_easy as te

# Input variables
start_date = "2018-08-01"

#Twitter API credentials
tweet_api = te.tweet_easy(filename_credentials = '/Users/ana/Documents/Twitter/twitter-credentials.json')


controlIdFolder = "controlFolder/"
outputFolder = "downloadedTweets/"

# Search terms
listqueries = ["btc"]

#now = datetime.datetime.now().date()
#days = [str(now - datetime.timedelta(days=i)) for i in range(7)]

for searchQuery in listqueries:
    print(searchQuery)
    tweet_api.download2csv(searchQuery = searchQuery, maxTweets = 10, tweetsPerQry = 10,
                        result_type = "mixed",
                        controlIdFolder = controlIdFolder, outputFolder = outputFolder)
