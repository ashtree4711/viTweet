from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import vi_twitter.search as search

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return 'The viTweet start page'

def convo(tweetID):
    return 'A viTweet conversation page showing the conversation starting from the Tweet with ID {}'.format(tweetID)

@app.route('/convo/<tweetID>/linear')
def conversation(tweetID):
    # Call function with TWEET-ID + max. Replies (please don't call over 10!)
    # content -> Temporary String (nothing for future)
    # response -> Dictionary to be used 
    content, response = search.get_replies(1069660787722084352, 5)
    return convo(tweetID) + render_template('conversation.html',response=response)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # Run without debug #app.run()
    