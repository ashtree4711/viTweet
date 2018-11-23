'''
Created on 20 Nov 2018

@author: markeschweiler
'''
import datetime, os, json
from pathlib import Path

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