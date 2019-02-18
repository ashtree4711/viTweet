from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap

#from vi_twitter.search import get_conversation
import vi_twitter.search as search
import matplotlib.pyplot as plt
import networkx as nx


app = Flask(__name__)
app.secret_key = 'some_secret'
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

@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
    if request.method == 'POST':
        requestedTweetID = request.form.get('tweetID')
        language = request.form.get('langopt')
    
        #if len(requestedTweetID) != 19:
        #   flash('Invalid ID, please try again!')
        #    return redirect(url_for('index'))
        #else: 
        #    return render_template('conversation.html', response=search.get_replies(requestedTweetID, language, 10))
        #search.get_conversation(requestedTweetID, language, max_replies=200)
        return render_template('conversation.html', response=search.get_conversation(requestedTweetID, language, max_replies=200))

@app.route('/network', methods=['GET', 'POST'])
def network():
    requestedTweetID = request.form.get('tweetID')
    language = request.form.get('langopt')
    G = nx.star_graph(7)
    pos = nx.spring_layout(G)
    colors = range(7)
    nx.draw_networkx_nodes(G, pos,nodelist=search.get_conversation(requestedTweetID, language, max_replies= 200),node_color='y',node_size=1000,alpha=0.8)
    nx.draw_networkx_nodes(G, pos,nodelist=search.get_conversation(requestedTweetID, language, max_replies= 200),node_color='r',node_size=500,alpha=0.8)
    nx.draw_networkx_nodes(G, pos,nodelist=search.get_conversation(requestedTweetID, language, max_replies= 200),node_color='b',node_size=500,alpha=0.8)
    # edges 
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,edgelist=[('1.tweet','2.replies')],width=8, alpha=0.5, edge_color='r')
    nx.draw_networkx_edges(G, pos,edgelist=[('1.tweet','3.quote_tweets')],width=8, alpha=0.5, edge_color='b')
    labels = {}
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    plt.axis('off')
    plt.savefig('network.png')
    return render_template('network.html', name = plt.show(), url ='network.png')   


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # To run without debug: #app.run()
    