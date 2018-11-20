'''
Created on 20 Nov 2018

@author: markeschweiler
'''
from vi_twitter.connector import connect_to_api

def search_tweets(keyword):
    twitter_session=connect_to_api()
    tweetList = []
    #get Tweets via API
    tweets = twitter_session.search(q=keyword, count=100, result_type='recent')
    if tweets.get('statuses'):
        for tweet in tweets['statuses']:
            tweetList.append(tweet)
    return tweetList


def search_retweets_by_id():
    twitter_session=connect_to_api()
    tweetList = []
   
    tweets = twitter_session.get_retweets(id=1064540462848098304)
    for tweet in tweets:
        tweetList.append(tweet)
        print(tweet)
    
    return tweetList