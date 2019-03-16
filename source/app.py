from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from flask_bootstrap import Bootstrap
import datetime
import configparser

import vi_twitter.search as search
import vi_twitter.utilities as utilities
import vi_network.network as network



    # Instantiate configparser and say which INI file to read the configurations from.
    # (The config is used to access for example the file paths defined in an INI file. 
    # Therefore the paths can be updated in the INI file at any time without requiring any changes elsewhere.)
config = configparser.ConfigParser()
config.read('config/app_config.ini')


app = Flask(__name__, static_url_path='/static')
app.secret_key = config['FLASKAPP']['APP_SECRET_KEY'] #app.config['APP_SECRET_KEY']
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/conversation', methods=['POST'])
def conversation():    
        # Save parameters from form input
    requestedTweetID = request.form.get('tweetID')
    language = request.form.get('langopt')
    visualization_type = request.form.get('visopt')
    
        # Start a new cookie session for searching
    session['session_type'] = 'search'
    mode = session['session_type']
    
        # Search for the conversation, save it as a JSON, return the filename of the JSON as 'basis' for the visualization
    print('INFO: Searching for the conversation starting from Tweet ', requestedTweetID)
        # Search for the conversation:
        # Call get_conversation() which executes the query and saves the result in a flat and a recursive JSON file
        # Then later use those JSON files to do something with the search results
    basis = search.get_conversation(requestedTweetID, language, max_replies=200)
    print("basis: ", basis)
    
        # Complete data of cookie session with the JSON filenames
        # TODO: @elli more èxplanation?
    basis_recursive = basis['recursive']
    basis_flat = basis['flat']
    session['r'] = basis_recursive
    session['f'] = basis_flat
    #session['basis'] = basis
    print("SESSION INFORMATION conversation(): ", session)

        # Depending on the type of visualization selected, redirect to the corresponding URL and pass along the values 'mode' and 'basis'
    if visualization_type=='list':
            # Use recursive list as basis for list visualizations
        session['current_basis'] = 'recursive'
        print("SESSION INFORMATION (for list): ", session)
            # session[session['current_session']] in this case is the value of 'basis_r', i.e. the filename of the recursive list
        return redirect(url_for('list_visualization', mode=mode, use_basis=basis_recursive, other_basis=basis_flat))
    elif visualization_type=='graph':
            # Use flat list as basis for graph visualizations
        session['current_basis'] = 'flat'
        print("SESSION INFORMATION (for graph): ", session)
        return redirect(url_for('graph_visualization', mode=mode, use_basis=basis_flat, other_basis=basis_recursive))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
        # Save parameters from form input
    visualization_type = request.form.get('visopt')
    
        # Start a new session with an uploaded file
    session['session_type'] = 'upload'
    mode = session['session_type']

        # Save the JSON file uploaded by the user
        #TODO: Zuerst überprüfen, ob es eine valide Datei ist?
        #TODO: Handle whether the user is uploading a flat or recursive file
    f = request.files['file']
    import_filename = 'fList_import_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # TODO: Use separate directory "config['FILES']['USERUPLOAD_JSON_FILES']" instead?
    f.save(config['FILES']['TEMP_JSON_FLATLIST'] + '/' + import_filename + '.json', buffer_size=16384)
    print('UPLOADED FILE SAVED AS: ', config['FILES']['TEMP_JSON_FLATLIST'] + import_filename + '.json')
    
        # Load the conversation from the imported file instead of performing a search; use the filename of the JSON as 'basis' for the visualization
    print('INFO: Using an imported JSON file to load the conversation')
    
    root_id = utilities.json_to_dictionary(mode, import_filename)['conversation'][0]['tweet_id']
    print("root_id: ", root_id)
    
        # Use the uploaded JSON file to do something with the results saved in it
        # Complete data of cookie session with the JSON filenames
        # TODO: @elli more èxplanation?
    rList = utilities.create_rList(root_id, import_filename)
    print("rList: ", rList)
    basis_recursive = utilities.save_rList(rList)
    print("basis_recursive: ", basis_recursive)
    basis_flat = import_filename
    session['r'] = basis_recursive
    session['f'] = basis_flat
    #session['basis'] = basis
    print("SESSION INFORMATION conversation(): ", session)

        # Depending on the type of visualization selected, redirect to the corresponding URL and pass along the values 'mode' and 'basis'
    if visualization_type=='list':
            # Use recursive list as basis for list visualizations
        session['current_basis'] = 'recursive'
        print("SESSION INFORMATION (for list): ", session)
            # session[session['current_session']] in this case is the value of 'basis_r', i.e. the filename of the recursive list
        return redirect(url_for('list_visualization', mode=mode, use_basis=basis_recursive, other_basis=basis_flat))
    elif visualization_type=='graph':
            # Use flat list as basis for graph visualizations
        session['current_basis'] = 'flat'
        print("SESSION INFORMATION (for graph): ", session)
        return redirect(url_for('graph_visualization', mode=mode, use_basis=basis_flat, other_basis=basis_recursive))


@app.route('/conversation/list', methods=['POST','GET'])
def list_visualization():
    if 'current_basis' in session:
            # Request the arguments that were passed with the redirect
        mode = request.args['mode']
        use_basis = request.args['use_basis']
        other_basis = request.args['other_basis']
        print("SESSION INFORMATION for list_visualization(): ", session)
        #print("mode: ", mode)
        #print("basis: ", basis)
            # TODO: @Lara: Hier stattdessen Template für Listen-Ansicht aufrufen, oder? (bzw. das bisher conversation.html heißende Template dazu nutzen)
        return render_template('conversation.html', response=utilities.json_to_dictionary(mode, use_basis), mode=mode, use_basis=use_basis, other_basis=other_basis)
    else:
        return 'Error while retrieving session information. Please start a new search.'


@app.route('/conversation/graph', methods=['POST','GET'])
def graph_visualization():
    if 'current_basis' in session:
            # Request the arguments that were passed with the redirect
        mode = request.args['mode']
        use_basis = request.args['use_basis']
        other_basis = request.args['other_basis']
        print("SESSION INFORMATION for graph_visualization(): ", session)
        
            # Call the function which plots the graph; the return value is the name of the JSON file storing the graph
        graph_data_filename, alert_message = network.draw_network(use_basis)
        
        return render_template('graph.html', response=utilities.json_to_dictionary(mode, use_basis), mode=mode, use_basis=use_basis, other_basis=other_basis, graph_data_filename=graph_data_filename, alert_message=alert_message)

    else:
        return 'Error while retrieving session information. Please start a new search.'


@app.route('/graph-data/<path:graph_data_filename>', methods=['POST', 'GET'])
def graph_data(graph_data_filename):
    #return send_file('../temp_files/json/graph/graph.json')
    #return send_file('static/graph.json')
    return send_from_directory(config['FILES']['TEMP_JSON_GRAPH'], graph_data_filename  + '.json') #return send_file(config['FILES']['TEMP_JSON_GRAPH'] + graph_data_filename + ".json")
    #return send_file(url_for('static', filename='graph.json'))


@app.route('/download/json/<path:json_filename>', methods=['GET'])
def download_json(json_filename):
        # Take the requested file from the path specified in the config; serve file at /download/[...].json
    if json_filename[0:6] == 'fList_':
        return send_from_directory(config['FILES']['TEMP_JSON_FLATLIST'], json_filename  + '.json')
    elif json_filename[0:6] == 'rList_':
        return send_from_directory(config['FILES']['TEMP_JSON_RECURSIVELIST'], json_filename  + '.json')
    else:
        return print("Download Error")


@app.route('/download/xml/<path:create_xml_filename>', methods=['GET'])
def download_xml(create_xml_filename):
        # Convert the currently shown JSON to XML
    xml_filename = utilities.json_to_xml(create_xml_filename)
        # Take the requested file from the path specified in the config; serve file at /download/[...].xml
        # TODO: Aus irgendeinem Grund fehlt der heruntergeladenen Datei die Endung '.xml'???
    return send_from_directory(config['FILES']['TEMP_XML_FILES'], xml_filename + '.xml')



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # To run without debug: #app.run()