'''
Created on 20 Nov 2018

@author: markeschweiler
'''
import datetime, os, json, xmltodict
from pathlib import Path
from builtins import int


def save_to_json(dictionary):
    '''
        Saves Dictionaries to JSON -> Dictionaries: https://www.python-kurs.eu/dictionaries.php
    '''
    now = datetime.datetime.now()
    persist_data = { 'datetime': now.strftime("%Y-%m-%d %H:%M:%S"),'export':dictionary}
    dirname = Path(__file__).parents[2]
    filename = now.strftime("%Y%m%d%H%M%S")
    persist_data_file = os.path.join(dirname, "temp_files/json/", filename + ".json") #TODO: Pfad stattdessen aus config-Datei entnehmen
    with open(persist_data_file, 'w') as outfile:
        json.dump(persist_data, outfile, indent=4, sort_keys=True)
    print ("SAVE JSON TO:", persist_data_file)
        
    return filename



def json_to_dictionary(mode, requested_file):
    if mode == 'search':
        json_file = open('../temp_files/json/' + requested_file + '.json') #TODO: Pfad stattdessen aus config-Datei entnehmen
    elif mode == 'upload':
        json_file = open('../useruploads/json/' + requested_file + '.json') #TODO: Pfad stattdessen aus config-Datei entnehmen
    json_str = json_file.read()
    dictionary = json.loads(json_str)
    
    return dictionary



def json_to_xml(json_filename):
    # Transform a file from JSON to XML, using the library xmltodict
    
        # Specify file names and paths
    xml_filename = json_filename
    json_filepath = '../temp_files/json/' + json_filename + '.json' #TODO: Pfad stattdessen aus config-Datei entnehmen
    xml_filepath = '../temp_files/xml/' + xml_filename + '.xml' #TODO: Pfad stattdessen aus config-Datei entnehmen
    
    with open(json_filepath, 'r') as f:
        jsonString = f.read()
    jsonString_with_added_root_element = '{"conversation":\n' + jsonString + '\n}'    
    xmlString = xmltodict.unparse(json.loads(jsonString_with_added_root_element), pretty=True)
    
    with open(xml_filepath, 'w', encoding="utf-8") as f:
        f.write(xmlString)
        
    return xml_filename



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
        



    
    
    
    
    
    
    

    
    