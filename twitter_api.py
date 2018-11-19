'''
Created on 16 Nov 2018

@author: markeschweiler
'''
import time
'''
# Created on 18.08.2018
# Hier werden Suchanfragen über die Twitter-API geregelt
# Die Zugriffe auf die Twitter-API sind begrenzt. Die 15 Zugriffe pro Viertelstunde können aber meist überschritten werden.
# @author: Mark Eschweiler
'''

from twython import Twython
import configparser

'''config['TWITTER']['API_key']'''
'''config['TWITTER']['API_secret_key']'''
    # Initializing Twitter Session
config = configparser.ConfigParser()
config.read('config/config.ini')
APP_KEY = 'dDyu1XBASytdT98LhO3jt4u8U'                                          
APP_SECRET = 'vdOKFu3JI4KRKfUdOiUIEuskUBgUbfER55ra5ZrsvsMQPEKLgq'           
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
def search_tweets(keyword):
        
    tweetList = []
    #get Tweets via API
    tweets = twitter.search(q=keyword, count=100, result_type='recent')
    if tweets.get('statuses'):
        for tweet in tweets['statuses']:
            tweetList.append(tweet)
    return tweetList


def search_retweets_by_id():
    tweetList = []
    time.sleep(1)
    tweets = twitter.get_retweets(id=1064540462848098304)
    for tweet in tweets:
        tweetList.append(tweet)
        print(tweet)
    
    return tweetList
    
                
    
    