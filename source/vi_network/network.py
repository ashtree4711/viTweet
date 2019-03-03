from flask import send_file
import matplotlib.pyplot as plt
import networkx as nx

import vi_twitter.utilities as utilities



    # TODO: This is very long... Vielleicht lässt sich das noch abkürzen
def extract_nodes_edges(flatList_dict):
    
    print("\nEXTRACTING TWEET-REPLY/TWEET-QUOTETWEET PAIRS FROM FLATLIST:")   
    
     
        # Go through all tweets in the flatList and extract the IDs for all of the tweet-reply pairs
    tweet_parent_id_r=[]
    tweet_child_id_r=[]
    for i, val in enumerate(flatList_dict['conversation']):
        tweet_parent_id_r.append(val['tweet_id'])
        
        if val['replies_id']: # If the list 'replies_id' contains something...
            
            if len(val['replies_id'])==1: # If the list 'replies_id' contains only one reply...
                tweet_child_id_r.append(val['replies_id'][0]) # Use the first (and only) element in the list 'replies_id'
                
            else: # If the list 'replies_id' contains more than one reply...
                for reply_i, reply_val in enumerate(val['replies_id']): # Go through the whole list 'replies_id'
                    if reply_i>0:
                        tweet_parent_id_r.append(val['tweet_id']) # Keep using the value of the tweet/tweet_parent_id_r for all the replies/tweet_child_id_rren
                    tweet_child_id_r.append(val['replies_id'][reply_i])
                    
        else: # If the list 'replies_id' is empty, do not add this pair to the list
            tweet_parent_id_r.pop()
        '''else: # If the list 'replies_id' is empty, give it the value 'no_replies'
            tweet_child_id_r.append('no_replies')'''
    
    tweet_reply_pairs = list(zip(tweet_parent_id_r, tweet_child_id_r))
    print("tweet_reply_pairs (", len(tweet_reply_pairs), ") : ", tweet_reply_pairs)
    
    
        # Go through all tweets in the flatList and extract the IDs for all of the tweet-quotetweet pairs
    tweet_parent_id_q=[]
    tweet_child_id_q=[]
    for i, val in enumerate(flatList_dict['conversation']):
        tweet_parent_id_q.append(val['tweet_id'])
        
        if val['quotedTweets']: # If the list 'replies_id' contains something...
            
            if len(val['quotedTweets'])==1: # If the list 'replies_id' contains only one reply...
                tweet_child_id_q.append(val['quotedTweets'][0]) # Use the first (and only) element in the list 'replies_id'
                
            else: # If the list 'replies_id' contains more than one reply...
                for reply_i, reply_val in enumerate(val['quotedTweets']): # Go through the whole list 'replies_id'
                    if reply_i>0:
                        tweet_parent_id_q.append(val['tweet_id']) # Keep using the value of the tweet/tweet_parent_id for all the replies/tweet_child_idren
                    tweet_child_id_q.append(val['quotedTweets'][reply_i])
                    
        else: # If the list 'quotedTweets' is empty, do not add this pair to the list
            tweet_parent_id_q.pop()
        '''else: # If the list 'quotedTweets' is empty, give it the value 'no_quote_tweets'
            tweet_child_id_q.append('no_quote_tweets')'''


    tweet_quotetweet_pairs = list(zip(tweet_parent_id_q, tweet_child_id_q))
    print("tweet_quotetweet_pairs (", len(tweet_quotetweet_pairs), "): ", tweet_quotetweet_pairs)
    
    
    all_tweet_pairs = tweet_reply_pairs + tweet_quotetweet_pairs
    print("all_tweet_pairs (", len(all_tweet_pairs), "): ", all_tweet_pairs)
    
    
        #TODO: Start-ID anders holen?
    if tweet_parent_id_r:
        start_tweet_id = tweet_parent_id_r[-1] 
    else: # In case there are no replies, only quotetweets
        start_tweet_id = tweet_parent_id_q[-1]
    all_tweet_nodes = [start_tweet_id] # Add the start tweet ID to the new list
    print("start_tweet_id: ", start_tweet_id)
    
    
    for i, val in enumerate(tweet_child_id_r):
        all_tweet_nodes.append(val)
    for i, val in enumerate(tweet_child_id_q):
        all_tweet_nodes.append(val)
    print("all_tweet_nodes (", len(all_tweet_nodes), "): ", all_tweet_nodes)
    
    
        # Find out how many unique pairs / values there are --> it seems that this difference causes problems in some cases
        # TODO: solve problem with duplicates in pairs / nodes list
    all_unique_tweet_pairs = set(all_tweet_pairs)
    print("all_unique_tweet_pairs (", len(all_unique_tweet_pairs), "): ", all_unique_tweet_pairs)
    all_unique_tweet_nodes = set(all_tweet_nodes)
    print("all_unique_tweet_nodes (", len(all_unique_tweet_nodes), "): ", all_unique_tweet_nodes)
    
    
    type_of_node = ['start']
    for i in tweet_parent_id_r:
        type_of_node.append('reply')
    for i in tweet_parent_id_q:
        type_of_node.append('quote_tweet')
    print("type_of_node (", len(type_of_node), "):", type_of_node)
    
    
    return all_tweet_nodes, all_tweet_pairs, type_of_node



def draw_network(flatList_filename):
    flatList_dict = utilities.json_to_dictionary(mode='visualize', requested_file=flatList_filename)
    
    
        # Extract the nodes and edges from the flat file used as basis for the visualization
    all_tweet_nodes, all_tweet_pairs, type_of_node = extract_nodes_edges(flatList_dict)


        # Undirected graph
    #G = nx.Graph()
        # Directed graph
    G = nx.DiGraph()
        # Star graph --> TODO: Der hat alle Replies und Quotetweets in einer Ebene, lässt sich das korrigieren?
    #num=len(all_tweet_nodes)-1
    #G = nx.star_graph(n=num, create_using=nx.Graph())
    
    
        # Add nodes from list 'all_tweet_nodes' 
    G.add_nodes_from(all_tweet_nodes)
        # Add edges from list 'all_tweet_pairs'
    G.add_edges_from(all_tweet_pairs)
    
    
        # Define colors for each type of node
    color_for_nodetype = []
    size_for_nodetype = []
    for x in type_of_node:
        if x == 'start':
            color_for_nodetype.append('red')
            size_for_nodetype.append(2000)
        elif x == 'reply':
            color_for_nodetype.append('blue')
            size_for_nodetype.append(500)
        elif x == 'quote_tweet':
            color_for_nodetype.append('green')
            size_for_nodetype.append(500)
    print("color_for_nodetype (", len(color_for_nodetype), "): ", color_for_nodetype)
    print("size_for_nodetype (", len(size_for_nodetype), "): ", size_for_nodetype)
            
        
        # TODO: Let nodes have meaningful positions / choose a better layout!
    #pos = nx.spring_layout(G)
    
    
        # TODO: evtl. besser wieder mit nx.draw_networkx_edges / _nodes / _labels arbeiten?
        
        # Draw the graph G; different layouts possible
        # node_color and node_size: as defined above
        # arrowstyle: see https://matplotlib.org/api/_as_gen/matplotlib.patches.ArrowStyle.html
        # node_shape: see https://matplotlib.org/api/markers_api.html
    #nx.draw_spring(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    #nx.draw_circular(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    #nx.draw_kamada_kawai(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    #nx.draw_shell(G, with_labels=True, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)
    nx.draw_spectral(G, with_labels=False, arrows=True, arrowstyle='-|>', node_color=color_for_nodetype, node_size=size_for_nodetype, node_shape='s', alpha=0.8)



        # Save the drawing to a PNG file and return the file
    plt.axis('off')
    plt.savefig('network.png')
        # Closing the plot prevents problems of a new graph getting added on top of the existing graph (for example, when refreshing the page)
    plt.close()
    #return render_template('network.html', nodelist=list_of_replies+list_of_quotetweets) #return render_template('network.html', name = plt.show(), url='network.png', response=response) #TODO: korrigieren; ich glaube name macht so keinen Sinn 
    return send_file('network.png')
