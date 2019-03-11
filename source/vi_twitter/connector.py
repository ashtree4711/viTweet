'''
Created on 16 Nov 2018

@author: markeschweiler
'''
import time
from pathlib import Path
from os.path import os
'''
# Created on 18.08.2018
# Hier werden Suchanfragen über die Twitter-API geregelt
# Die Zugriffe auf die Twitter-API sind begrenzt. Die 15 Zugriffe pro Viertelstunde können aber meist überschritten werden.
# @author: Mark Eschweiler
'''

from twython import Twython
import configparser


    # Initializing Twitter Session
def connect_to_api():
    '''
        @desc To connect to the Twitter-API with developer keys
    '''
        # Create relative Path
    dirname = Path(__file__).parents[1]
    config_path = os.path.join(dirname, 'config/config.ini')
        # Configuration Parser
    config = configparser.ConfigParser()
    config.read(config_path)
        # Establish Connection
    APP_KEY = config['TWITTER']['API_key']                                         
    APP_SECRET = config['TWITTER']['API_secret_key']
    #ACCESS_TOKEN  = config ['TWITTER']['Access_token']        
    twitter_session = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter_session.obtain_access_token()
    twitter_session = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    return twitter_session

    
                
    
    