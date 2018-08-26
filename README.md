# twitter-btc
Sentiment analysis for btc tweets

# Instructions to get started.
1. First of all you will need a Twitter API access token in order to download tweets. You can get this by creating a Twitter app at https://developer.twitter.com/en/apply.
2. You will need python 3.6 installed and the following libraries:
- tweepy
- json (pre-installed)
- pandas
- numpy
- datetime
- os (pre-installed)
- re (pre-installed)
- nltk (pre-installed)

(You can install each one of them using pip install module_name in the command line)

3. Fill in the access token information in a json file. You can see the format in credentials_example.json.

4. Open the file 00_donwload_tweets.py and modify the file location for credentials, output folders and query search.

5. Run 00_download_tweets.py in the command line (type __python 00_download_tweets.py__ in the command line from the same directory where 00_donwload_tweets.py is located). This file will download tweets to the outputFolder location specified.

6. Run 01_add_sentiment.py in order to add the sentiment column to the downloaded files. In case the outputFolder was modified, this parameter also needs to be modified in the script.

Enjoy the tweets!
