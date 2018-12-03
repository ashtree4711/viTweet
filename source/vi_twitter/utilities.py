'''
Created on 20 Nov 2018

@author: markeschweiler
'''
import datetime, os, json
from pathlib import Path
from vi_twitter import TweetObject as Tweet

def save_to_json(dictionary):
        # Saves Dictionaries to JSON -> Dictionaries: https://www.python-kurs.eu/dictionaries.php
    now = datetime.datetime.now()
    persist_data = { 'datetime': now.strftime("%Y-%m-%d %H:%M"),'export':dictionary}
    dirname = Path(__file__).parents[2]
    persist_data_file = os.path.join(dirname, "temp_files/json/", now.strftime("%Y%m%d")+".json")
    with open(persist_data_file, 'w') as outfile:
        json.dump(persist_data, outfile, indent=4, sort_keys=True)
    print ("SAVE JSON TO:", persist_data_file)
    
    return

def create_response(searched_Tweet, replies):
    now = datetime.datetime.now()
    response = {'datetime': now.strftime("%Y-%m-%d %H:%M"), 'main':searched_Tweet, 'replies':replies}
    dirname = Path(__file__).parents[2]
    created_json_file = os.path.join(dirname, "temp_files/json/", "response"+now.strftime("%Y%m%d")+".json")
    with open(created_json_file, 'w') as outfile:
        json.dump(response, outfile, indent=4, sort_keys=True)
    print ("SAVE JSON TO:", created_json_file)
    return response



    
    
    
    
    
    
    

    
    