# viTweet

viTweet is a webservice providing visualizations to better understand Twitter conversations with their Replies and Quote Tweets that follow a selected Tweet.

| Program library | Usage |
| --- | --- |
| Twython 3.7 | Wrapper for Twitter API |
| Flask 1.0.2 | Web framework |
| Jinja2 2.10 | Template engine |
| D3.js v4 | Graph visualization |

Make sure to import the libraries or use the pipfile!


## How to use viTweet

### Accessing the Twitter API

* [Set up a Twitter developer account](https://developer.twitter.com/en/apply) if you do not already have one
* [Generate your access tokens](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)
* Enter your access tokens to the /source/config/config.ini

### Running the application
* Use an IDE like Eclipse (others have not yet been tested by us) to run the file 'app.py'

* Run via command line
```shell
$ cd viTweet/source/ # Change to where the directory containing 'app.py' is located
$ export FLASK_APP=app.py
$ export FLASK_ENV=development # To run with debugger
$ flask run
```

### Basic usage
* Open the URL indicated in the console output in your brower (usually http://127.0.0.1:5000/)
* Enter a Tweet URL or ID into the search bar
* Try the different visualization options
 * List visualization
 ![list view](/screenshots/list-1.png "List View")
 ![list view](/screenshots/list-2.png "List View")
 * Graph visualization
 ![graph view](/screenshots/graph.png "Graph View")
image ...
* Export and import conversations
 * Export search result in different formats with the button at the top right of the results page
 * Import a file (type 'flat JSON') with the uploader at the bottom of the index page

## Documentation
* see comments in the respective files
* see the [Wiki](https://github.com/ashtree4711/viTweet/wiki) for a more extensive documentation (in German)
