import networkx as nx
from networkx.readwrite import json_graph
import json
import datetime
import configparser

import vi_twitter.utilities as utilities



    # Instantiate configparser and say which INI file to read the configurations from
    # (The config is used to access for example the file paths defined in an INI file. 
    # Therefore the paths can be updated in the INI file at any time without requiring any changes elsewhere.)
config = configparser.ConfigParser()
config.read('config/app_config.ini')



def extract_nodes_edges(flatList_dict):
    
    print("\nEXTRACTING NODES AND EDGES FOR TWEET-REPLY/TWEET-QUOTETWEET PAIRS FROM FLATLIST")
    
    
        # Go through all tweets in the flatList and extract the IDs for all of the tweet-reply pairs (= edges)
    tweet_reply_parent=[]
    tweet_reply_child=[]
    for i, val in enumerate(flatList_dict['conversation']):
        tweet_reply_parent.append(val['tweet_id'])
        if val['replied_by']: # If the list 'replied_by' contains something...
            if len(val['replied_by'])==1: # If the list 'replied_by' contains only one reply...
                tweet_reply_child.append(val['replied_by'][0]) # Use the first (and only) element in the list 'replied_by'
            else: # If the list 'replied_by' contains more than one reply...
                for reply_i, reply_val in enumerate(val['replied_by']): # Go through the whole list 'replied_by'
                    if reply_i>0:
                        tweet_reply_parent.append(val['tweet_id']) # Keep using the value of the tweet/tweet_reply_parent for all the replies/tweet_reply_children
                    tweet_reply_child.append(val['replied_by'][reply_i])
        else: # If the list 'replied_by' is empty, do not add this pair to the list
            tweet_reply_parent.pop()
        '''else: # If the list 'replied_by' is empty, give it the value 'no_replies'
            tweet_reply_child.append('no_replies')'''
    
    tweet_reply_pairs = list(zip(tweet_reply_parent, tweet_reply_child))
    print("Edges for the Replies (", len(tweet_reply_pairs), ") : ", tweet_reply_pairs)
    
    
        # Go through all tweets in the flatList and extract the IDs for all of the tweet-quotetweet pairs
    tweet_quotetweet_parent=[]
    tweet_quotetweet_child=[]
    for i, val in enumerate(flatList_dict['conversation']):
        tweet_quotetweet_parent.append(val['tweet_id'])
        if val['quoted_by']: # If the list 'quoted_by' contains something...
            if len(val['quoted_by'])==1: # If the list 'quoted_by' contains only one reply...
                tweet_quotetweet_child.append(val['quoted_by'][0]) # Use the first (and only) element in the list 'quoted_by'
            else: # If the list 'quoted_by' contains more than one reply...
                for quotetweet_i, quotetweet_val in enumerate(val['quoted_by']): # Go through the whole list 'quoted_by'
                    if reply_i>0:
                        tweet_quotetweet_parent.append(val['tweet_id']) # Keep using the value of the tweet/tweet_parent_id for all the replies/tweet_child_idren
                    tweet_quotetweet_child.append(val['quoted_by'][quotetweet_i])
        else: # If the list 'quoted_by' is empty, do not add this pair to the list
            tweet_quotetweet_parent.pop()


    tweet_quotetweet_pairs = list(zip(tweet_quotetweet_parent, tweet_quotetweet_child))
    print("Edges for the Quote Tweets (", len(tweet_quotetweet_pairs), "): ", tweet_quotetweet_pairs)
    
    
    edges = tweet_reply_pairs + tweet_quotetweet_pairs
    print("All edges (", len(edges), "): ", edges)
    
    
        # Save all tweets as nodes in the format {'A TWEET ID': {'tweet_id': 'A TWEET ID', 'node_label': 'BLABLABLA', ...}}
        # TODO: This does not have (explicit) information about the type of node (like 'start', 'reply', or 'quote_tweet')
    nodes = {}
    for i, val in enumerate(flatList_dict['conversation']):
        nodes[val['tweet_id']] = {}
        nodes[val['tweet_id']].update(flatList_dict['conversation'][i])        
    print("All nodes: ", nodes)
    
    
        # Return the nodes and edges extracted from the fList
    return nodes, edges



def draw_network(flatList_filename):
        # Get the dict equivalent of the fList 
    flatList_dict = utilities.json_to_dictionary(mode='visualize', requested_file=flatList_filename)
        
        # Extract the nodes and edges from the fList file used as basis for the visualization
    nodes, edges = extract_nodes_edges(flatList_dict)


    print("\nCREATING GRAPH...")

        # Directed graph
    G = nx.DiGraph()
    
        # Add the nodes to the graph
    G.add_nodes_from(nodes)
    
        # Add the edges from the list 'edges' to the graph
    G.add_edges_from(edges)
    
        # Draw the graph
    nx.draw(G)
    
        # Add other Tweet attributes to the nodes saved in graph G, which are needed for the visualization
    for n in G:
        G.node[n]['tweet_id'] = n
        G.node[n]['tweet_content'] = nodes[n]['tweet_content']
        G.node[n]['user_name'] = nodes[n]['user']['user_name']
        G.node[n]['screen_name'] = nodes[n]['user']['screen_name']
        G.node[n]['timestamp'] = nodes[n]['timestamp']
        
            # Save the Tweet types: 
            # The Root Tweet, i.e. the one that was searched for, is the last one of the nodes (because it is last in 
            # the fList), therefor check whether the currently iterated one is the last one, if so it is the Root Tweet
        if n == list(G.node.keys())[-1]:
            G.node[n]['tweet_type'] = 'root_tweet'
            # Identify Replies and Quote Tweets depending on the values of 'reply_to' and 'quote_to' for each Tweet
        else:
            if nodes[n]['reply_to'] != None:
                G.node[n]['tweet_type'] = 'reply'
            elif nodes[n]['quote_to'] != None:
                G.node[n]['tweet_type'] = 'quote_tweet'
        
            # To access profile pictures, use the redirect to the image file that Twitter offers as https://twitter.com/
            # [screen_name]/profile_image?size=normal (small version) or alternatively use "size=original" (larger version)
        profile_picture = 'https://twitter.com/' + nodes[n]['user']['screen_name'] + '/profile_image?size=normal'
        G.node[n]['profile_picture'] = profile_picture

    
        # Write the 'node_link_data' into a JSON file, i.e. the nodes with the attributes added above and the links between them 
        # The JSON file can then be loaded with D3 to create an interactive graph in the browser
    d = json_graph.node_link_data(G)
    print("Data contained in graph G: ", d)
    
    print("\nSAVING GRAPH...")
    graph_filename = "graph_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print("Graph saved as: ", graph_filename + ".json")
    json.dump(d, open(config['FILES']['TEMP_JSON_GRAPH'] + graph_filename + ".json",'w'))
    
    
        # Return the filename of the JSON file where the data of the created graph is stored for later use
    return graph_filename
