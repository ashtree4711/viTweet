"""
@desc: This is the main program and webservice: Handles all routing, search queries, file uploads
Session cookies are used to store the following information:
- 'basis_flat': filename 'fList_TIMESTAMP' of the fList JSON
- 'basis_recursive': filename 'rList_TIMESTAMP' of the rList JSON
- 'mode': either 'search' or 'upload'
"""

from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from flask_bootstrap import Bootstrap
import datetime
import configparser

import vi_twitter.search as search
import vi_twitter.utilities as utilities
import vi_network.network as network


# Instantiate configparser and specify which INI file to read the configurations from
# The config is used to access the filesystem paths defined in the INI file, so the paths can be updated in the INI file
# at any time without requiring changes elsewhere.
config = configparser.ConfigParser()
config.read('config/app_config.ini')



# Configure the Flask app
app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key = config['FLASKAPP']['APP_SECRET_KEY']
Bootstrap(app)



@app.route('/')
def index():
    """
    @desc: Routing for URL '/' (index page)
    
    @return: Render the template 'index.html'
    """
    return render_template('index.html')


@app.route('/about')
def about():
    """
    @desc: Routing for URL '/about' (about page)
    
    @return: Render the template 'about.html'
    """
    return render_template('about.html')


@app.route('/contact')
def contact():
    """
    @desc: Routing for URL '/contact' (contact page)
    
    @return: Render the template 'contact.html'
    """
    return render_template('contact.html')


@app.route('/query', methods=['POST'])
def query():
    """
    @desc: Routing for URL '/query' (called from search form on index page)
    Performs the search query with search.get_conversation()
    
    @return: Redirect to URL '/conversation/list' or '/conversation/graph', depending on the chosen visualization option
    """
    # Request parameters from form input
    root_tweet_id = request.form.get('tweetID')
    language = request.form.get('langopt')
    visualization_type = request.form.get('visopt')
    print('INFO: Searching for the conversation starting from Tweet ', root_tweet_id)
    
    # The function search.get_conversation() performs the query and saves the results as fList and rList JSON files
    # Returned as 'query_result_filenames' is a dict containing both the rList and the fList JSON filename
    query_result_filenames = search.get_conversation(root_tweet_id, language, max_replies=200)
    
    # Set up the cookie session for searching
    session['mode'] = 'search'
    session['basis_recursive'] = query_result_filenames['recursive']
    session['basis_flat'] = query_result_filenames['flat']
    print("\nSESSION INFORMATION: ", session)
    
    # Redirect to the URL for list or graph visualization with URL parameters 'mode' and 'basis'
    # (= rList for list visualization, fList for graph visualization)
    if visualization_type=='list': 
        return redirect(url_for('list_visualization', mode=session['mode'], basis=session['basis_recursive']))
    elif visualization_type=='graph':
        return redirect(url_for('graph_visualization', mode=session['mode'], basis=session['basis_flat']))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    @desc: Routing for URL '/upload' (called from file upload form on index page)
    Saves the fList JSON file uploaded by the user and creates the corresponding rList JSON file from it
        
    @return: Redirect to URL '/conversation/list' or '/conversation/graph', depending on the chosen visualization option
    """
    # Request parameters from form input
    visualization_type = request.form.get('visopt')
    
    # Save the JSON file uploaded by the user, using a filename in the style 'fList_import_TIMESTAMP'
    f = request.files['file']
    import_filename = 'fList_import_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    f.save(config['FILES']['TEMP_JSON_FLATLIST'] + '/' + import_filename + '.json', buffer_size=16384)
    print('UPLOADED FILE SAVED AS: ', config['FILES']['TEMP_JSON_FLATLIST'] + import_filename + '.json')
    
    # Read the Root Tweet ID from the imported fList (the Root Tweet is the last element in the fList)
    fList = utilities.json_to_dictionary(import_filename)
    root_tweet_id = fList['conversation'][-1]['tweet_id']   
    print('INFO: Using an imported JSON file to load the conversation starting from Tweet', root_tweet_id)

    # Create the rList from the fList JSON file uploaded by the user
    rList = utilities.create_rList(root_tweet_id, import_filename)
    
    # Set up the cookie session for file upload
    session['mode'] = 'upload'
    session['basis_recursive'] = utilities.save_rList(rList)
    session['basis_flat'] = import_filename
    
    print("SESSION INFORMATION: ", session)
    
    # Redirect to the URL for list or graph visualization with URL parameters 'mode' and 'basis'
    # (= rList for list visualization, fList for graph visualization)
    if visualization_type=='list': 
        return redirect(url_for('list_visualization', mode=session['mode'], basis=session['basis_recursive']))
    elif visualization_type=='graph':
        return redirect(url_for('graph_visualization', mode=session['mode'], basis=session['basis_flat']))


@app.route('/conversation/list', methods=['POST','GET'])
def list_visualization():
    """
    @desc: Routing for URL '/conversation/list'
    
    @return Render template 'converation.html'
    """
    # Pass multiple parameters to the template: 'response' is the dict of the chosen JSON file; 'mode', 'use_basis', 
    # and 'other_basis' are taken from what is stored in the session cookie
    return render_template('conversation.html', response=utilities.json_to_dictionary(session['basis_recursive']), mode=session['mode'], use_basis=session['basis_recursive'], other_basis=session['basis_flat'])


@app.route('/conversation/graph', methods=['POST','GET'])
def graph_visualization():
    """
    @desc: Routing for URL '/conversation/graph'
    Calls network.draw_network() which plots the graph and saves it in a JSON file 
    
    @return Render template 'graph.html'
    """
    # Returned as 'graph_data_filename' is the filename where the graph is stored, as 'graph_data_filename' a message that may need to be displayed to the user
    graph_data_filename, alert_message = network.draw_network(session['basis_flat'])
    
    # Pass multiple parameters to the template: 'response' is the dict of the chosen JSON file; 'mode', 'use_basis', and 'other_basis'
    # are taken from what is stored in the session cookie; 'graph_data_filename' and 'alert_message' were returned by network.draw_network() above
    return render_template('graph.html',response=utilities.json_to_dictionary(session['basis_flat']), mode=session['mode'], use_basis=session['basis_flat'], other_basis=session['basis_recursive'], graph_data_filename=graph_data_filename, alert_message=alert_message)


@app.route('/graph-data/<path:graph_data_filename>', methods=['POST', 'GET'])
def graph_data(graph_data_filename):
    """
    @desc: Routing for URL '/graph-data/<path:graph_data_filename>'
    Delivers the graph JSON file when it is used to load the graph data in graph.json
    
    @param graph_data_filename: filename without file extension of a JSON file storing a graph

    @return Send from the directory the JSON graph file
    """
    return send_from_directory(config['FILES']['TEMP_JSON_GRAPH'], graph_data_filename  + '.json')


@app.route('/download/json/<path:json_filename>', methods=['POST', 'GET'])
def download_json(json_filename):
    """
    @desc: Routing for URL '/download/json/<path:json_filename>'
    Deliver from its directory the JSON file fList, rList, or graph which the user wants to download
    
    @param json_filename: filename without file extension of a fList, rList, or graph JSON file
    
    @return Send from the directory the fList, rList, or graph JSON file requested by user for download
    """
    # The type of file requested is determined by the prefix of the JSON filename 
    if json_filename[0:6] == 'fList_':
        return send_from_directory(config['FILES']['TEMP_JSON_FLATLIST'], json_filename  + '.json')
    
    elif json_filename[0:6] == 'rList_':
        return send_from_directory(config['FILES']['TEMP_JSON_RECURSIVELIST'], json_filename  + '.json')

    elif json_filename[0:6] == 'graph_':
        return send_from_directory(config['FILES']['TEMP_JSON_GRAPH'], json_filename  + '.json')


@app.route('/download/xml/<path:json_filename>', methods=['GET'])
def download_xml(json_filename):
    """
    @desc: Routing for URL '/download/xml/<path:json_filename>'
    Creates the XML file which the user wants to download by converting the rList JSON file to its XML equivalent
    and delivers it from its directory
    
    @param json_filename: filename without file extension of the rList JSON file from which to create the XML file
    
    @return: Send from the directory the XML file requested by user for download
    """
    xml_filename = utilities.json_to_xml(json_filename)
    
    return send_from_directory(config['FILES']['TEMP_XML_FILES'], xml_filename + '.xml')



# As long as this module is the main program, run the app: either in debug mode (show debugger, automatically reload
# app whenever a change in the source files is detected) or without debug
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #app.run()
