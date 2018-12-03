'''
Created on 20 Nov 2018

@author: markeschweiler
'''
import datetime, os, json
from pathlib import Path
from vi_twitter import TweetObject as Tweet
from builtins import int

def save_to_json(dictionary):
    '''
        Saves Dictionaries to JSON -> Dictionaries: https://www.python-kurs.eu/dictionaries.php
    '''
    now = datetime.datetime.now()
    persist_data = { 'datetime': now.strftime("%Y-%m-%d %H:%M"),'export':dictionary}
    dirname = Path(__file__).parents[2]
    persist_data_file = os.path.join(dirname, "temp_files/json/", now.strftime("%Y%m%d")+".json")
    with open(persist_data_file, 'w') as outfile:
        json.dump(persist_data, outfile, indent=4, sort_keys=True)
    print ("SAVE JSON TO:", persist_data_file)
    
    return

def create_response(searched_Tweet, replies):
    '''
        Creates the response after searching and filtering Tweets
    '''
    now = datetime.datetime.now()
    response = {'datetime': now.strftime("%Y-%m-%d %H:%M"), 'main':searched_Tweet, 'replies':replies}
    dirname = Path(__file__).parents[2]
    created_json_file = os.path.join(dirname, "temp_files/json/", "response"+now.strftime("%Y%m%d")+".json")
    with open(created_json_file, 'w') as outfile:
        json.dump(response, outfile, indent=4, sort_keys=True)
    print ("SAVE JSON TO:", created_json_file)
    return response

def preprocess_input(input):
    '''
        Checks if the input is the required tweet_id as an Integer and changes if it is not so. 
    '''
    if isinstance(input, int):
        print("input: ", input)
        print("isInputInteger: ", isinstance(input, int))
        print("isInputString: ", isinstance(input, str))
        print("no processing required...")
        return input
    if isinstance(input, str):
        print("input: ", input)
        print("isInputInteger: ", isinstance(input, int))
        print("isInputString: ", isinstance(input, str))
        print("processing required...")
        input=int(input[-19:])
        print("processedInput: ", input)
        print("isInputInteger: ", isinstance(input, int))
        print("isInputString: ", isinstance(input, str))
        return input
        



    
    
    
    
    
    
    

    
    