'''
Created on 20 Nov 2018
    The search.py module constructs the search query, initiates access to the Twitter API and processes the results. 
@author: markeschweiler
'''
import twython

import vi_twitter.TweetObject as Tweet
from vi_twitter.connector import connect_to_api
from vi_twitter.utilities import preprocess_input, \
    save_rList, save_fList, create_rList


def get_conversation(userInput, language, max_replies):
    """
    @param userInput: Serves a String or an Integer which contains the Twitter-ID of a Tweet 
    @param language: restricts tweets to the given language, given by an ISO 639-1 code
    @param max_replies: maximum replies per call
    
    @return response: Contains the complete conversation followed by the given tweet ID in a
    Py-Dictionary
    
    @desc This main function calls the needed functions for the whole process and gives the whole Dictionary
    back to the webservice
    """
        # Establish a session to the twitter-api.
    twitterSession = connect_to_api()
    
        # Convert the userInput to the needed Tweet-ID as an Integer
    root_id=preprocess_input(userInput)
    
    
        # Initially we do need the Tweet-Object of the Root-Tweet, to call the get_replies()-function.
    rootTweet = get_tweet_by_id(root_id, twitterSession)
        
        # Initialize a fList (flat list), where all tweets get stored. Save it to a JSON-File
    fList=[]
    fList=get_replies(twitterSession, rootTweet, language, max_replies, fList)

    fList_filename = save_fList(fList)
    
        # Create a rList (recursive list), which represents the structure better. Save it to a JSON-File
    rList=create_rList(root_id, fList_filename)
    rList_filename = save_rList(rList)
    
        # Return the filenames for the recursive and flat list, so they can be used to create the requested visualisations
        # This way, no new request to the Twitter API has to be made when reloading the page or switching visualisation types 
    json_filename = {'recursive': rList_filename, 'flat': fList_filename}


  
    return json_filename
    

def get_replies(twitterSession, tweet, language, max_replies, fList):
    """
        @param twitterSession: needs a consisting connection to twitter-api    
        @param tweet: TweetObject of Tweet for which we searching replies
        @param language: restricts tweets to the given language, given by an ISO 639-1 code
        @param max_replies: maximum replies per call
        @param fList: Is the list which stores all results
        
        @return fList: Returns updated list back to every older instance of recursive method. The list is flat, not hierarchical.
        
        @desc The function has a recursive structure. For each reply, the method calls itself according to the depth-first 
        principle until the tweet under investigation no longer has any replies. Then a dictionary is built up, which
         recursively completes itself until all replies and their replies are contoured. 
    """
    print("___________________________________________")
    print("INFO: INVESTIGATING REPLIES OF TWEET", tweet.get_tweet_id(), " (", tweet.get_user_screenname(),")")
    potentialReplies=[]
    replyHits= []
    previousPotentialReplies=0
    
        # Query is a construction for the workaround. Because you can't explicitly search for replies in the Twitter API. 
        # All potential tweets have to be searched first. This query searches for all tweets from and to the originator of
        # the tweet to be examined.
    query="to:"+tweet.get_user_screenname()+" OR from:"+tweet.get_user_screenname()+" OR "+"https://twitter.com/" + tweet.get_user_screenname() + "/status/" + tweet.get_tweet_id_str()+ " -filter:retweets"
    print(query)
    
        # We need the parameter "since_id" first, because the API will give us automatically the latest tweets
        # and we just have to take care, that no Tweet should be older than the Root Tweet.
    potentialReplies, replyHits=search_by_usermention_since_id(query, twitterSession, potentialReplies, replyHits, tweet, language)
    
        # Now, we need the max_id since the every call to API will give us, as already said, the latest tweet.
        # So we do need Tweets, which are older than the already received Tweets. We get them, if we take the last
        # Tweet of the existing list and declare it as the max_id.
    while (len(replyHits) <= max_replies and previousPotentialReplies < len(potentialReplies) and potentialReplies[-1].get_tweet_id() > tweet.get_tweet_id()):
        previousPotentialReplies=len(potentialReplies)
        potentialReplies, replyHits=search_by_usermention_max_id(query, twitterSession, potentialReplies, replyHits, tweet, language)

        # Clean the hits necessary, because within a API-Call, there could be more than the demanded score. So we reduce the quantity if we do not need all
        # replies
    replyHits=clean_hits(replyHits, max_replies)

        # We finally know how many replies the tweet has and so save this information within the TweetObject
    #tweet.set_reply_quantity(len(replyHits))
    
        # Produce some control information shown in the console
    print("INFO: ", len(potentialReplies),"TWEETS BROWSED")
    print("INFO: ", tweet.get_reply_quantity(), "REPLIES IDENTIFIED")
    print("INFO: ", tweet.get_quote_tweet_quantity(), "QUOTES IDENTIFIED")
    print("INFO: FOLLOWING ID's ARE REPLIES")
    for t in tweet.get_replied_by_list():
            print("--> ", t)
    print("INFO: FOLLOWING ID's ARE QUOTES")
    for t in tweet.get_quoted_by_list():
        print("--> ", t)
            
        # If the replyHits-list in this instance is not 0, go through the list and call a new instance for every hit. After that,
        # construct a new Dictionary from the tweet and its replies of the current instance. 
 
    if len(replyHits)!=0:
        for hit in replyHits:
            get_replies(twitterSession, hit, language, max_replies, fList)
        fList.append(tweet.convert_to_new_dict())
        return fList
    else:
        fList.append(tweet.convert_to_new_dict())
        return fList
       

def get_tweet_by_id(tweet_id, session):
    """
        @param tweet_id: Tweet-ID as Integer
        @params session: needs a consisting connection to twitter-api
        
        @return tweet: Returns a Tweet as TweetObject
        @desc Gets just one Tweet by its ID and constructs 
    """
    twitterTweet = session.show_status(id=tweet_id)
    tweet = Tweet.Tweet(twitterTweet)
    return tweet

def search_by_usermention_since_id(userMention, session, potentialReplies, replyHits, rootTweet, language):
    """
        @param userMention: '@user'-String expecting
        @param session: Connection to Twitter-API via Twython needed
        @param potentialReplies: List of all received Tweets(Object) as potential Replies -> needed to always the same 100 Tweets
        @param replyHits: List of all hitted Reply-Tweets(Object)
        @param rootTweet: Tweet(Object) for which we seek replies #
        
        @return Updated lists of potentialReplies & replyHits. These are the latest tweets
        
        @desc Calls the first 100 Tweets. They have to be older than related tweet  
    """
    try:
        newTweets=session.search(q=userMention, count=100, lang=language, result_type='recent', since_id=rootTweet.get_tweet_id())
        if newTweets.get('statuses'):
            for tweet in newTweets['statuses']:
                    # create a tweet object
                tweetObj=Tweet.Tweet(tweet)
                    # remind all potential hits
                potentialReplies.append(tweetObj)
                    # if the potential hit has in its attribute "reply_to_tweet_id" the same number as the tweet_id of investigated tweet.
                    # put the information into the investigated tweet object, raise the counter and append to list of hits.
                if tweetObj.get_reply_to_tweet_id()==rootTweet.get_tweet_id():
                    rootTweet.set_replied_by_list(tweetObj.get_tweet_id())
                    rootTweet.raise_reply_quantity()
                    replyHits.append(tweetObj)
                    # same as above, just with quoted tweets
                if tweetObj.get_quote_to_tweet_id()==rootTweet.get_tweet_id():
                    rootTweet.set_quoted_by_list(tweetObj.get_tweet_id())
                    rootTweet.raise_quote_tweet_quantity()
                    replyHits.append(tweetObj)
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
    return potentialReplies, replyHits


def search_by_usermention_max_id(userMention, session, potentialReplies, replyHits, rootTweet, language):
    """ 
        @param userMention: '@user'-String expecting
        @param session: Connection to Twitter-API via Twython needed
        @param potentialReplies: List of all received Tweets(Object) as potential‚ Replies -> needed to always the same 100 Tweets
        @param replyHits: List of all hitted Reply-Tweets(Object)
        @param rootTweet: Tweet(Object) for which we seek replies 
        @return Updated lists of potentialReplies & replyHits
        
        @desc After we got the first 100 tweets, which are the latest, we need the next 100 tweets that should be older than the
        last of the potentialReplies-list. But the tweets are not allowed to be older than rootTweet, so we dont browser tweets where 
        replies are not possible.
    """
    try:
        newTweets=session.search(q=userMention, count=100, lang=language, result_type='recent', max_id=potentialReplies[-1].get_tweet_id()-1)
        if newTweets.get('statuses'):
            for tweet in newTweets['statuses']:
                    # detailed information in search_by_usermention_since_id()
                tweetObj = Tweet.Tweet(tweet)
                potentialReplies.append(tweetObj)
                if tweetObj.get_reply_to_tweet_id()==rootTweet.get_tweet_id():
                    rootTweet.set_replied_by_list(tweetObj.get_tweet_id())
                    rootTweet.raise_reply_quantity()
                    replyHits.append(tweetObj)
                if tweetObj.get_quote_to_tweet_id()==rootTweet.get_tweet_id():
                    rootTweet.set_quoted_by_list(tweetObj.get_tweet_id())
                    rootTweet.raise_quote_tweet_quantity()
                    replyHits.append(tweetObj)      
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
    return potentialReplies, replyHits
   
def clean_hits(replyHits, max_replies):
    """
        @param replyHits: List of all Replies
        @param max_replies: The maximum parameter
        
        @return newReplyHits: to the maximum reduced list
        
        @desc If we got more replies than we need, we reduced the list to maximum
    """
    newReplyHits=[]
    for reply in replyHits[0:max_replies]:
        newReplyHits.append(reply)
    return newReplyHits

def convert_list_to_dict(tweetObjectList):
    '''
        @param tweetObjectList: a list with tweet-object
        @return newTweetObjectList: a list with tweet-objects as dictionaries
        @desc Each tweet object is written to a Dictionary so that the Web service can read it.
    '''
    newTweetObjectList=[]
    for tweetObject in tweetObjectList:
        newTweetObjectList.append(tweetObject.convert_to_new_dict())
    return newTweetObjectList
            
    
    
    
      
    
    

    