import json

from flask import send_file
from networkx.readwrite import json_graph

import matplotlib.pyplot as plt
import networkx as nx
import vi_twitter.utilities as utilities


    # TODO: This is very long... Vielleicht lässt sich das noch abkürzen
def extract_nodes_edges(flatList_dict):
    
    print("\nEXTRACTING TWEET-REPLY/TWEET-QUOTETWEET PAIRS FROM FLATLIST:")
    
    
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
    print("Edges for the replies (= tweet-reply pairs) (", len(tweet_reply_pairs), ") : ", tweet_reply_pairs)
    
    
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
        '''else: # If the list 'quoted_by' is empty, give it the value 'no_quote_tweets'
            tweet_quotetweet_child.append('no_quote_tweets')'''

    tweet_quotetweet_pairs = list(zip(tweet_quotetweet_parent, tweet_quotetweet_child))
    print("Edges for the quotetweets (= tweet-quotetweet pairs) (", len(tweet_quotetweet_pairs), "): ", tweet_quotetweet_pairs)
    
    
    all_tweet_pairs = tweet_reply_pairs + tweet_quotetweet_pairs
    print("All edges (", len(all_tweet_pairs), "): ", all_tweet_pairs)
    
    
        #TODO: Start-ID anders holen?
    if tweet_reply_parent:
        start_tweet_id = tweet_reply_parent[-1] 
    elif tweet_reply_parent: # In case there are no replies, only quotetweets
        start_tweet_id = tweet_quotetweet_parent[-1]
    else:
        return print("Error: This tweet has not been replied to or quoted")
    all_tweet_nodes = [start_tweet_id] # Add the start tweet ID to the new list
    print("start_tweet_id: ", start_tweet_id)
    
    
    for i, val in enumerate(tweet_reply_child):
        all_tweet_nodes.append(val)
    for i, val in enumerate(tweet_quotetweet_child):
        all_tweet_nodes.append(val)
    print("all_tweet_nodes (", len(all_tweet_nodes), "): ", all_tweet_nodes)
    
    
        # Save all tweets as nodes in the format {'A TWEET ID': {'tweet_id': 'A TWEET ID', 'node_label': 'BLABLABLA', ...}}
        # TODO: This does not have (explicit) information about the type of node (like 'start', 'reply', or 'quote_tweet')
    nodes = {}
    for i, val in enumerate(flatList_dict['conversation']):
        nodes[val['tweet_id']] = {}
            # Create labels for the nodes (instead the elements could also be taken one by one by the D3 script
        nodes[val['tweet_id']]['node_label'] = flatList_dict['conversation'][i]['tweet_content'] + "\n—" + flatList_dict['conversation'][i]['user']['user_name'] + "(@" + flatList_dict['conversation'][i]['user']['screen_name'] + ")"
        nodes[val['tweet_id']].update(flatList_dict['conversation'][i])        
    print("Nodes (= tweets): ", nodes)
    
    
        # Save the node labels separately
    labels = {}
    for i, val in enumerate(nodes):
        labels[val] = nodes[val]['node_label']
    print("Labels: ", labels)
    
    
        # Types of nodes ('start', 'reply', or 'quote_tweet')
    types_of_nodes = ['start']
    for i in tweet_reply_parent:
        types_of_nodes.append('reply')
    for i in tweet_quotetweet_parent:
        types_of_nodes.append('quote_tweet')
    print("Types of nodes (", len(types_of_nodes), "):", types_of_nodes)
    
    
    '''    # Find out how many unique pairs / values there are --> it seems that this difference causes problems in some cases
        # TODO: solve problem with duplicates in pairs / nodes list
    all_unique_tweet_pairs = set(edges)
    print("all_unique_tweet_pairs (", len(all_unique_tweet_pairs), "): ", all_unique_tweet_pairs)
    all_unique_tweet_nodes = set(all_tweet_nodes)
    print("all_unique_tweet_nodes (", len(all_unique_tweet_nodes), "): ", all_unique_tweet_nodes)'''
    
    
    all_tweet_contents= []
    for i,val in enumerate(flatList_dict['conversation']):
        all_tweet_contents.append(val['tweet_content'])
    start_tweet_contents = all_tweet_contents[-1]
    all_tweet_contents.insert(0, start_tweet_contents)
    all_tweet_contents = all_tweet_contents[:-1]
    print("Tweet contents (",len(all_tweet_contents), "):", all_tweet_contents)
    
    
    return nodes, labels, all_tweet_nodes, all_tweet_pairs, types_of_nodes, all_tweet_contents #return all_tweet_nodes, all_tweet_pairs, types_of_nodes, all_tweet_contents #return all_tweet_nodes, edges, types_of_nodes, all_tweet_contents



def draw_network(flatList_filename):
    flatList_dict = utilities.json_to_dictionary(mode='visualize', requested_file=flatList_filename)
        
        # Extract the nodes and edges from the flat file used as basis for the visualization
    nodes, labels, all_tweet_nodes, edges, types_of_nodes, all_tweet_contents = extract_nodes_edges(flatList_dict) #all_tweet_nodes, edges, types_of_nodes, all_tweet_contents = extract_nodes_edges(flatList_dict)


        # Undirected graph
    #G = nx.Graph()
        # Directed graph
    G = nx.DiGraph()
    
        # Star graph --> TODO: Der hat alle Replies und Quotetweets in einer Ebene, lässt sich das korrigieren?
    #num=len(all_tweet_nodes)-1
    #G = nx.star_graph(n=num, create_using=nx.Graph())
    
    
    all_labels=[] 
    for a, b in zip(all_tweet_nodes,all_tweet_contents):
        string = str(a)+ ": " + b
        all_labels.append(string)
    print('Labels:', all_labels)

        #nodes labels
    labels2 = dict(zip(all_tweet_nodes, all_labels))
    
        # Add the nodes to the graph
    G.add_nodes_from(nodes) #G.add_nodes_from(all_tweet_nodes)
    
        # Add the edges from the list 'edges' to the graph
    G.add_edges_from(edges)
    
    
        # Define colors for each type of node
    color_for_nodetype = []
    size_for_nodetype = []
    
    for item in types_of_nodes:
        if item == 'start':
            color_for_nodetype.append('red')
            size_for_nodetype.append(2000)
        elif item == 'reply':
            color_for_nodetype.append('blue')
            size_for_nodetype.append(500)
        elif item == 'quote_tweet':
            color_for_nodetype.append('green')
            size_for_nodetype.append(500)
    print("Colors for nodetypes (", len(color_for_nodetype), "): ", color_for_nodetype)
    print("Sizes for nodetypes (", len(size_for_nodetype), "): ", size_for_nodetype)
    
    
        # TODO: Let nodes have meaningful positions / choose a better layout!
    pos = nx.shell_layout(G)
    
        # TODO: evtl. besser wieder mit nx.draw_networkx_edges / _nodes / _labels arbeiten?
        
        # Draw the graph G; different layouts possible
        # node_color and node_size: as defined above
        # arrowstyle: see https://matplotlib.org/api/_as_gen/matplotlib.patches.ArrowStyle.html
        # node_shape: see https://matplotlib.org/api/markers_api.html
    #nx.draw_spring(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    #nx.draw_circular(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    #nx.draw_kamada_kawai(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    nx.draw_shell(G) #nx.draw_shell(G, with_labels = False, arrows=True, arrowstyle='-|>', node_shape='s', alpha=0.8) #nx.draw_shell(G, with_labels = False, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)    #nx.draw_spectral(G,  with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    
    
    nx.draw_networkx_labels(G, pos, labels=labels2, font_size =8, font_color ='k', font_family = 'sans-serif', alpha= 0.8)
    
    
        # Save the drawing to a PNG file and return the file
    plt.axis('off')
    plt.savefig('../temp_files/png/network.png')
    
    
        # Interactive graph
    #i=0
    for n in G:
        G.node[n]['tweet_id'] = n
        G.node[n]['tweet_content'] = nodes[n]['tweet_content']
        G.node[n]['user_name'] = nodes[n]['user']['user_name']
        G.node[n]['screen_name'] = nodes[n]['user']['screen_name']
        G.node[n]['timestamp'] = nodes[n]['timestamp']
        
            # Save Tweet types, depending on the values of 'reply_to' and 'quote_to' for each Tweet
        if nodes[n]['reply_to'] != None:
            G.node[n]['tweet_type'] = 'reply'
        elif nodes[n]['quote_to'] != None:
            G.node[n]['tweet_type'] = 'quote_tweet'
        else:
            G.node[n]['tweet_type'] = 'root_tweet'
        
            # To access profile pictures, use the redirect to the image file that Twitter offers as https://twitter.com/[screen_name]/profile_image?size=normal (for a small version; use "size=original" for a larger version)
        profile_picture = 'https://twitter.com/' + nodes[n]['user']['screen_name'] + '/profile_image?size=normal'
        G.node[n]['profile_picture'] = profile_picture
        #i=i+1
    
    
        # Give other attributes besides an ID to the graph's list of nodes
    for n in nodes: #for n in all_tweet_nodes:
        G.node[n]['label'] = nodes[n]['node_label'] #G.node[n]['label'] = all_tweet_nodes[n]['node_label'] # TODO: is this adding the correct labels?
        
        # Write the 'node_link_data' into a JSON file, this will contain the attributes added above
        # The JSON file can then be loaded with D3 to create an interactive graph in the browsesr
    d = json_graph.node_link_data(G)
    print("d: ", d)
    #graph_filename = '../temp_files/json/graph/graph_' + flatList_filename[6:] + '.json'
    graph_filename = 'static/graph.json'
    print("graph_filename: ", graph_filename)
    json.dump(d, open(graph_filename,'w'))
    
    
        # Closing the plot prevents problems of a new graph getting added on top of the existing graph (for example, when refreshing the page)
    plt.close()
    #return render_template('network.html', nodelist=list_of_replies+list_of_quotetweets) #return render_template('network.html', name = plt.show(), url='network.png', response=response) #TODO: korrigieren; ich glaube name macht so keinen Sinn 
    return send_file('../temp_files/png/network.png')
    
