import tweepy #https://github.com/tweepy/tweepy
import os
import datetime
import json
import numpy as np
import pandas as pd
import re


class tweet_easy():
    def __init__(self, filename_credentials = None):
        if filename_credentials is None:
            filename_credentials = '/Users/ana/Documents/Twitter/twitter-credentials.json'
        json_data = open(filename_credentials).read()
        credentials = json.loads(json_data)
        auth = tweepy.AppAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)
        self.api = api

    def download2json(self, searchQuery = None, maxTweets = 1000000000, tweetsPerQry = 100, until = None, result_type = "mixed",
                  geocode=None, lang = 'en',
        controlIdFolder = "/Users/u553574/Documents/Personal/genioAI/tweets/crypto_continuous_download/",
        outputFolder = "/Users/u553574/Documents/Personal/genioAI/tweets/crypto_continuous_download/tweets/"):
        if searchQuery is None:
            print("searchQuery parameter is empty, please enter a search term")
            return(None)
        api = self.api
        # file locations
        filename_sinceId = controlIdFolder + searchQuery + "_sinceId.txt"
        filename_max_id = controlIdFolder + searchQuery + "_max_id.txt"
        outputFile = outputFolder + datetime.datetime.now().strftime(searchQuery + "_%Y%m%d%H%M%S.json")

        # If results from a specific ID onwards are reqd, set since_id to that ID.
        # else default to no lower limit, go as far back as API allows
        if os.path.exists(filename_sinceId):
            with open(filename_sinceId) as f:
                sinceId = int(f.read())
        else:
            sinceId = None

        # If results only below a specific ID are, set max_id to that ID.
        # else default to no upper limit, start from the most recent tweet matching the search query.
        if os.path.exists(filename_max_id):
            with open(filename_max_id) as f:
                max_id = int(f.read())
        else:
            max_id = -1


        tweetCount = 0
        print("Downloading max {0} tweets".format(maxTweets))
        with open(outputFile, 'w')  as f:
            f.write("[")
            while tweetCount < maxTweets:
                try:
                    if (until is None):
                        if (max_id <= 0):
                            if (not sinceId):
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        result_type=result_type, geocode=geocode)
                            else:
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        since_id=sinceId, result_type=result_type, geocode=geocode)
                        else:
                            if (not sinceId):
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        max_id=str(max_id - 1), result_type=result_type, geocode=geocode)
                            else:
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        max_id=str(max_id - 1), result_type=result_type, geocode=geocode,
                                                        since_id=sinceId)
                    else:
                        if (max_id <= 0):
                            if (not sinceId):
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        until=until, result_type=result_type, geocode=geocode)
                            else:
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        since_id=sinceId, until=until, result_type=result_type, geocode=geocode)
                        else:
                            if (not sinceId):
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        max_id=str(max_id - 1), until=until, result_type=result_type, geocode=geocode)
                            else:
                                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = lang, include_entities = True,
                                                        max_id=str(max_id - 1), until=until, result_type=result_type, geocode=geocode,
                                                        since_id=sinceId)
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    for tweet in new_tweets:
                        json.dump(tweet._json, f, sort_keys = True, indent = 4)
                        f.write(",")
                    tweetCount += len(new_tweets)
                    max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break

        with open(outputFile, 'r+') as f:
            f.seek(0,2)                 # end of file
            size=f.tell()               # the size...
            f.truncate(size-1)
        with open(outputFile, "a") as f:
            f.write("]")

        print("Downloaded {0} tweets".format(tweetCount))

        # print max_id to file
        if max_id is not None:
            with open(filename_max_id, "w") as f:
                f.write(str(max_id))

        # print sinceId to file
        if sinceId is not None:
            with open(filename_sinceId, "w") as f:
                f.write(str(sinceId))

        print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, outputFile))
        return(None)

    def download2csv(self, searchQuery = None, maxTweets = 1000000000, tweetsPerQry = 100, until = None, result_type = "mixed",
                  geocode=None, lang = 'en',
        controlIdFolder = "/Users/u553574/Documents/Personal/genioAI/tweets/crypto_continuous_download/",
        outputFolder = "/Users/u553574/Documents/Personal/genioAI/tweets/crypto_continuous_download/tweets/"):
        if searchQuery is None:
            print("searchQuery parameter is empty, please enter a search term")
            return(None)
        api = self.api
        # file locations
        filename_sinceId = controlIdFolder + searchQuery + "_sinceId.txt"
        filename_max_id = controlIdFolder + searchQuery + "_max_id.txt"
        outputFile = outputFolder + datetime.datetime.now().strftime(searchQuery + "_%Y%m%d%H%M%S.csv")

        # If results from a specific ID onwards are reqd, set since_id to that ID.
        # else default to no lower limit, go as far back as API allows
        if os.path.exists(filename_sinceId):
            with open(filename_sinceId) as f:
                sinceId = int(f.read())
        else:
            os.makedirs(controlIdFolder, exist_ok = True)
            sinceId = None

        # If results only below a specific ID are, set max_id to that ID.
        # else default to no upper limit, start from the most recent tweet matching the search query.
        if os.path.exists(filename_max_id):
            with open(filename_max_id) as f:
                max_id = int(f.read())
        else:
            os.makedirs(controlIdFolder, exist_ok = True)
            max_id = -1


        # Preparation of call to api
        args = dict()
        args['q'] = searchQuery
        args['count'] = tweetsPerQry
        if lang is not None:
            args['lang'] = lang
        args['include_entities'] = True
        args['result_type'] = result_type
        if geocode is not None:
            args['geocode'] = geocode
        if until is not None:
            args['until'] = until
        if sinceId != False:
            args['sinceId'] = sinceId
        if max_id > 0:
            args['max_id'] = str(max_id - 1)


        tweetCount = 0
        list_jsons = []
        print("Downloading max {0} tweets".format(maxTweets))

        while tweetCount < maxTweets:
            try:
                new_tweets = api.search(**args)

                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    list_jsons.append(tweet._json)
                tweetCount += len(new_tweets)
                max_id = new_tweets[-1].id
                args['max_id'] = str(max_id - 1)
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break


        # print max_id to file
        if max_id is not None:
            with open(filename_max_id, "w") as f:
                f.write(str(max_id))

        # print sinceId to file
        if sinceId is not None:
            with open(filename_sinceId, "w") as f:
                f.write(str(sinceId))

        # If output format is csv
        df = self.prepareDF(pd.DataFrame(list_jsons), filter_en=False)
        os.makedirs(outputFolder, exist_ok = True)
        df.to_csv(outputFile, index=False)
        print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, outputFile))
        return(None)

    def prepareDF(self, df, filter_en=True):
        df["user_id"] = df["user"].apply(lambda x: x["id"])
        df["user_description"] = df["user"].apply(lambda x: x["description"])
        df["user_location"] = df["user"].apply(lambda x: x["location"])
        df["user_url"] = df["user"].apply(lambda x: x["url"])
        df["user_followers_count"] = df["user"].apply(lambda x: x["followers_count"])
        df["user_friends_count"] = df["user"].apply(lambda x: x["friends_count"]) # : number of users this account is following
        df["user_listed_count"] = df["user"].apply(lambda x: x["listed_count"]) # : number of public lists this user is a member of
        df["user_statuses_count"] = df["user"].apply(lambda x: x["statuses_count"]) # : The number of Tweets (including retweets issued by the user.
        df["user_created_at"] = df["user"].apply(lambda x: x["created_at"])
        df["user_utc_offset"] = df["user"].apply(lambda x: x["utc_offset"])
        df["user_lang"] = df["user"].apply(lambda x: x["lang"][0:2])
        df["createdts"] = pd.to_datetime(df.created_at, format="%a %b %d %H:%M:%S +0000 %Y", errors="coerce")
        df["date"] = df.createdts.apply(lambda x: x.date())

        df["source"] = df.source.apply(lambda x: re.sub(r"^<.+>(.+)<.+>$", "\\1", x))

        cols = ["created_at", "favorited", "geo", "id", "lang", "source", "text", "truncated", "user_id", "user_description",
        "user_location", "user_url", "user_followers_count", "user_friends_count", "user_listed_count",
        "user_statuses_count", "user_created_at", "user_utc_offset", "user_lang"]

        if (filter_en):
          df = df[cols][df.lang == "en"]
        else:
          df = df[cols]
        return(df)
