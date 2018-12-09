from flask import Flask, render_template, Request
from flask_bootstrap import Bootstrap

import vi_twitter.search as search
from flask.globals import request

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

def convo(tweetID):
    return 'A viTweet conversation page showing the conversation starting from the Tweet with ID {}'.format(tweetID)

@app.route('/convo/<tweetID>/linear', methods=['GET', 'POST'])
def conversation(tweetID):
    # Call function with TWEET-ID + max. Replies (please don't call over 10!)
    # content -> Temporary String (nothing for future)
    # response -> Dictionary to be used
    if request.method == 'POST':
        response = request.form['response']
    content, response = search.get_replies(response, 5)
    return convo(tweetID) + render_template('conversation.html',response=response)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # Run without debug #app.run()
    