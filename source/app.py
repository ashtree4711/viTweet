from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap

import vi_twitter.search as search

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
        search.get_conversation(requestedTweetID, language, max_replies=200)
        return #render_template('conversation.html', response=search.get_conversation(requestedTweetID, language, max_replies=10))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    # To run without debug: #app.run()
