import pymongo
import time
import logging
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import requests


def Reg(txt):
    mentions_regex= r'@[A-Za-z0-9_]+' #pattern to remove all @ mentions in the tweet
    url_regex= r'https?:\/\/\S+' #Pattern to remove all URL's
    hashtag_regex= r'#[A-Za-z0-9_]+' # pattern to remove  hashtag
    rt_regex= 'RT\s' # pattern to remove all retweets ie. RT
    txt = re.sub(mentions_regex, '', txt)  #removes @mentions
    txt = re.sub(hashtag_regex, '', txt) #removes hashtag symbol
    txt = re.sub(rt_regex, '', txt) #removes RT to announce retweet
    txt = re.sub(url_regex, '', txt) #removes most URLs
    return txt


# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongo_db_container", port=27017)

# Select the database you want to use withing the MongoDB server
db = client.mongo_db
collections = db.tweets

time.sleep(10)  # seconds


pg = create_engine('postgresql://chr_tweety:56786688@postgres_container:5432/tweety_db', echo=True)
webhook_url = "https://hooks.slack.com/services/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"

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')

analyzer = SentimentIntensityAnalyzer()
time.sleep(5)
docs = db.tweets.find()
for doc in docs:
    query = "INSERT INTO tweets VALUES (%s, %s);"
    text = doc['text']
    #'''
    re_text = Reg(text)
    score = analyzer.polarity_scores(re_text)['compound']
    print(score)
    pg.execute(query, (re_text, score))
    format = {"text": re_text,"score": score}

    requests.post(url=webhook_url, json = format)
    time.sleep(3)

logging.critical('*** etl.py has ended! ***')

#'''