from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

import vi_twitter.search as search

app = Flask(__name__)
Bootstrap(app)


def get_replies(tweetID, maxReplies):
    # Call function with TWEET-ID + max. Replies (please don't call over 10!)
    # content -> Temporary String (nothing for future)
    # response -> Dictionary to be used 
    content, response = search.get_replies(tweetID, maxReplies)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
    if request.method == 'POST':
        # maybe TODO: check if input is valid (only Twitter URL or ID accepted); if URL, convert to ID
        requestedTweetID = request.form.get('tweetID')
    return render_template('conversation.html',response=get_replies(requestedTweetID, 10))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # To run without debug: #app.run()
   
