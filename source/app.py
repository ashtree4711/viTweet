from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

import vi_twitter.search as search

app = Flask(__name__)
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
        # maybe TODO: check if input is valid (only Twitter URL or ID accepted); if URL, convert to ID
        requestedTweetID = request.form.get('tweetID')
        requestedLanguage = request.form.get('language')
    return render_template('conversation.html',response=search.get_replies(requestedTweetID, requestedLanguage, maxReplies=10))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # To run without debug: #app.run()
