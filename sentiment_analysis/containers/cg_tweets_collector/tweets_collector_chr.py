import collections
import pymongo
import tweepy
import logging
import time

conn = pymongo.MongoClient(host='mongo_db_container')

db = conn.mongo_db
collections = db.tweets
client = tweepy.Client(bearer_token="...")


logging.warning('---- Collecting tweets----')

search_query = "Python lang:en -is:retweet -is:reply"

cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    #id=user.id,
    query=search_query,
    #exclude=['retweets','replies'],
    tweet_fields=['text','created_at']
).flatten(limit=200)

for tweet in cursor:
    
    logging.warning('---- Inserting tweets to DB ----')
    collections.insert_one(tweet.data)

while(True):
    logging.critical('*** doing nothing ***')
    time.sleep(2)

