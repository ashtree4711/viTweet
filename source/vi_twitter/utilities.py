'''
Created on 20 Nov 2018

@author: markeschweiler
'''

from builtins import int
import configparser
import datetime, os, json, xmltodict
from pathlib import Path


    # Instantiate configparser and say which INI file to read the configurations from 
    # (The configparser is used to access the file paths defined in an INI file. 
    # Therefore the paths can be updated in the INI file at any time without requiring any changes here.)
config = configparser.ConfigParser()
config.read('config/app_config.ini')




def save_rList(dictionary):
    '''
        @param dictionary: saves a Python dictionary within a JSON-file for recursive list in the folder
        @desc Saves Dictionaries to JSON -> Dictionaries: https://www.python-kurs.eu/dictionaries.php
    '''
    now = datetime.datetime.now()
    persist_data = { 'datetime': now.strftime("%Y-%m-%d %H:%M:%S"),'conversation':dictionary}
    dirname = Path(__file__).parents[2]
    filename = "rList_"+now.strftime("%Y%m%d%H%M%S")
    persist_data_file = os.path.join(dirname, "temp_files/json/recursiveList/", filename + ".json") #TODO: Pfad stattdessen aus config-Datei entnehmen
    with open(persist_data_file, 'w') as outfile:
        json.dump(persist_data, outfile, indent=4, sort_keys=True)
    print ("SAVE RECURSIVE LIST TO:", persist_data_file)
    return filename

def save_fList(dictionary):
    '''
        @param dictionary: saves a Python dictionary within a JSON-file for recursive list in the folder
        @desc Saves Dictionaries to JSON -> Dictionaries: https://www.python-kurs.eu/dictionaries.php
    '''
    now = datetime.datetime.now()
    persist_data = { 'datetime': now.strftime("%Y-%m-%d %H:%M:%S"),'conversation':dictionary}
    dirname = Path(__file__).parents[2]
    filename = "fList_"+now.strftime("%Y%m%d%H%M%S")
    persist_data_file = os.path.join(dirname, "temp_files/json/flatList/", filename + ".json") #TODO: Pfad stattdessen aus config-Datei entnehmen
    with open(persist_data_file, 'w') as outfile:
        json.dump(persist_data, outfile, indent=4, sort_keys=True)
    print ("SAVE FLAT LIST TO:", persist_data_file)
    return filename


def json_to_dictionary(mode, requested_file):

    if mode == 'search' or mode == 'visualize':
        if requested_file[0] == 'r':
            json_file = open(config['FILES']['TEMP_JSON_RECURSIVELIST'] + requested_file + '.json')
        elif requested_file[0] == 'f':
            json_file = open(config['FILES']['TEMP_JSON_FLATLIST'] + requested_file + '.json') 

        # TODO: Use separate directory "config['FILES']['USERUPLOAD_JSON_FILES']" instead?
    elif mode == 'upload':
        if requested_file[0] == 'r':
            json_file = open(config['FILES']['TEMP_JSON_RECURSIVELIST'] + requested_file + '.json')
        elif requested_file[0] == 'f':
            json_file = open(config['FILES']['TEMP_JSON_FLATLIST'] + requested_file + '.json')

    json_str = json_file.read()
    dictionary = json.loads(json_str)
    
    return dictionary


def json_to_xml(json_filename):
    '''
    Transform a file from JSON to XML, using the library xmltodict
    '''
        # Specify file names and paths
    xml_filename = json_filename
    json_filepath = config['FILES']['TEMP_JSON_RECURSIVELIST'] + json_filename + '.json' #TODO: korrekt???
    xml_filepath = config['FILES']['TEMP_XML_FILES'] + xml_filename + '.xml' #TODO: korrekt???
    
    with open(json_filepath, 'r') as f:
        jsonString = f.read()
    jsonString_with_added_root_element = '{"conversation":\n' + jsonString + '\n}'    
    xmlString = xmltodict.unparse(json.loads(jsonString_with_added_root_element), pretty=True)
    
    with open(xml_filepath, 'w', encoding="utf-8") as f:
        f.write(xmlString)
        
    return xml_filename



def create_rList(tweet_id, fList_filename):

    '''
        @param tweet_id: the id of the investigated tweet
        @param fList_filename: the flat list of all tweets. All tweets are on the top level and are related per specific lists
        within the tweet
        @return rList: a list, where replied tweets are within the related tweet
        @desc: To simplify human reading, the flat tweet list should be recursively converted into a hierarchical list. Answers 
        or QuotedTweets to a certain tweet can be found within the examined tweet. These in turn possess answers or QuotedTweeets 
        themselves, which in turn should lie within them. The result is a list or dictionary in a tree structure. The function is 
        structured recursively according to the Depth-First schema. 
    '''
        # Use the flat list of tweets inside 'conversation' 
    fList = json_to_dictionary(mode='search', requested_file=fList_filename)['conversation']
    for investigatedTweet in fList:
        if investigatedTweet.get('tweet_id') == tweet_id:
            replyList=get_replies_from_fList(investigatedTweet, fList)
            if len(replyList)!=0:
                rList=[]
                rList2=[]
                for reply in replyList:
                    rList2.append(create_rList(reply.get('tweet_id'), fList_filename))
                rList={'inv.tweet':investigatedTweet, 'replies': rList2}
                return rList
            else:
                rList={'inv.tweet':investigatedTweet, 'replies':None}
                return rList


def get_replies_from_fList(investigatedTweet, fList):
    '''
        @param investigatedTweet: to Tweet for which we searching replies and quoted tweets
        @param fList: the complete list of all candidates
        @return replyList: a list with a tweets, which are replies or quoted tweets
        @desc Sub-function of create_rList. All replies and quoted tweets of the examined tweet are collected from the entire fList 
        using object parameters and packed into a separate list.
    '''
    replyList=[]
    for tweet in fList:
        if tweet.get('reply_to')==investigatedTweet.get("tweet_id") or tweet.get('quote_to')==investigatedTweet.get("tweet_id"):
            replyList.append(tweet)
    return replyList


def preprocess_input(input):
    '''
        @param input: the raw  user-input
        @return input: investigated and parsed input as Integer (not String)
        @desc Checks if the input is the required tweet_id as an Integer and changes if it is not so. 
    '''
    if isinstance(input, int):
        print("input: ", input)
        #print("isInputInteger: ", isinstance(input, int))
        #print("isInputString: ", isinstance(input, str))
        #print("no processing required...")
        return input
    if isinstance(input, str):
        print("input: ", input)
        #print("isInputInteger: ", isinstance(input, int))
        #print("isInputString: ", isinstance(input, str))
        #print("processing required...")
        input=int(input[-19:])
        #print("processedInput: ", input)
        #print("isInputInteger: ", isinstance(input, int))
        #print("isInputString: ", isinstance(input, str))
        return input
        



    
    
    
    
    
    
    

    
    