'''
Created on 16 Nov 2018

@author: markeschweiler
'''
'''
# Created on 18.08.2018
# This is where Twitter API searches are handled
# Access to the Twitter API is limited. 450 accesses are allowed with a free developer account.
# @author: Mark Eschweiler
'''
    # Initializing Twitter Session

import configparser
from os.path import os
from pathlib import Path

from twython import Twython


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

    
                
    
    