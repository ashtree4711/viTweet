'''
Created on 16 Nov 2018

@author: markeschweiler
'''
'''
# Created on 18.08.2018
# Hier werden Suchanfragen über die Twitter-API geregelt
# Die Zugriffe auf die Twitter-API sind begrenzt. Die 15 Zugriffe pro Viertelstunde können aber meist überschritten werden.
# @author: Mark Eschweiler
'''

from twython import Twython
import configparser



    # Zugangsdaten Twitter-API
config = configparser.ConfigParser()
config.read('config/config.ini')
APP_KEY = config['TWITTER']['API_key']
APP_SECRET = config['TWITTER']['API_secret_key']
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
def search_tweets(keyword):
        # Erzeuge leere Liste zum Speichern der rohen Tweets 
    tweetList = []

    tweets = twitter.search(q=keyword, count=100, result_type='recent')
    if tweets.get('statuses'):
        for tweet in tweets['statuses']:
            tweetList.append(tweet)
                

    return tweetList