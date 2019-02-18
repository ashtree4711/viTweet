'''
Created on 20 Nov 2018

@author: markeschweiler
'''
from vi_twitter.connector import connect_to_api
from vi_twitter.utilities import create_response, preprocess_input, save_to_json
import vi_twitter.TweetObject as Tweet
import twython

    
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
    quoteTweets=get_quote_tweets(twitterSession, rootTweet, language)
    replies=get_replies(twitterSession, rootTweet, language, max_replies)
    
        # merging the replies dict and the quoteTweets dict
    merged = {**quoteTweets, **replies}
    
        # saving temporary for test purposes
    #save_to_json(replies)
    #save_to_json(quoteTweets)
    save_to_json(merged)
    
    #return quoteTweets, replies
    #return response
    return merged
    

def get_replies(twitterSession, tweet, language, max_replies):
    """
    @param twitterSession: needs a consisting connection to twitter-api    
    @param tweet: TweetObject of Tweet for which we searching replies
    @param language: restricts tweets to the given language, given by an ISO 639-1 code
    @param max_replies: maximum replies per call
    
    @return response: Dict of Tweet with all its Replies in a list
    
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
    query="to:"+tweet.get_user_screenname()+" OR from:"+tweet.get_user_screenname()+" -filter:retweets"
        # We need the parameter "since_id" first, because the API will give us automatically the latest tweets
        # and we just have to take care, that no Tweet should be older than the Root Tweet.
    potentialReplies, replyHits=search_by_usermention_since_id(query, twitterSession, potentialReplies, replyHits, tweet, language)
    
        # Now, we need the max_id since the every call to API will give us, as already said, the latest tweet.
        # So we do need Tweets, which are older than the already received Tweets. We get them, if we take the last
        # Tweet of the existing list and declare it as the max_id.
    while (len(replyHits) <= max_replies and previousPotentialReplies < len(potentialReplies) and potentialReplies[-1].get_tweet_id() > tweet.get_tweet_id()):
        previousPotentialReplies=len(potentialReplies)
        potentialReplies, replyHits=search_by_usermention_max_id(query, twitterSession, potentialReplies, replyHits, tweet, language)
    
        # Clean the hits necessary, because within a API-Call, there could be more than the demanded score. So we reduce the quantity if need not all
        # replies
    replyHits=clean_hits(replyHits, max_replies)
    
        # We finally know how many replies the tweet has and so save this information within the TweetObject
    tweet.set_reply_quantity(len(replyHits))
    
        # Produce some control information shown in the console
    print("INFO: ", len(potentialReplies),"TWEETS BROWSED")
    print("INFO: ", len(replyHits), "REPLIES IDENTIFIED")
    if len(replyHits)!=0:
        print("INFO: FOLLOWING ID's ARE REPLIES")
        for hit in replyHits:
            print("------> ", hit.get_tweet_id())

        # If the replyHits-list in this instance is not 0, go through the list and call a new instance for every hit. After that,
        # construct a new Dictionary with the tweet and its replies of the current instance. Else, just construct a new Dictionary
        # with the Tweet and set the replies to null.
    if len(replyHits)!=0:
        responseList=[]
        for hit in replyHits:
            responseList.append(get_replies(twitterSession, hit, language, max_replies))
        response={'1.tweet': tweet.convert_to_new_dict(), '2.replies':responseList}   
        return response 
    else:
        response={'1.tweet':tweet.convert_to_new_dict(), '2.replies':None}
        return response
       
    
    
    
def get_replies2(tweet_id, language, max_replies=5):
        # tweet_id -> Twitter-URL or ID
        # language -> Restricts tweets to the given language, given by an ISO 639-1 code. Language detection is best-effort
        # max_replies -> maximum Replies
        
    twitterSession = connect_to_api() 
    potentialReplies=[]
    replyHits= []
    previousPotentialReplies=0
    
        # Convert user input to Twitter ID Integer
    tweet_id=preprocess_input(tweet_id)
    
    rootTweet = get_tweet_by_id(tweet_id, twitterSession)
        # create from the screenname a user mention
    userMention="to:"+rootTweet.get_user_screenname()+" OR from:"+rootTweet.get_user_screenname()+" -filter:retweets"
 
        # First Round: We need the parameter "since_id" first, because the API will give us automatically the latest tweets
        #              and we just have to take care, that no Tweet should be older than the Root Tweet.
    potentialReplies, replyHits=search_by_usermention_since_id(userMention, twitterSession, potentialReplies, replyHits, rootTweet, language)
        # Second Round: Now, we need the max_id since the every call to API will give us, as already said, the latest tweet.
        #               So we do need Tweets, which are older than the already received Tweets. We get them, if we take the last
        #               Tweet of the existing list and declare it as the max_id.
    while (len(replyHits) <= max_replies and previousPotentialReplies < len(potentialReplies) and potentialReplies[-1].get_tweet_id() > rootTweet.get_tweet_id()):
        previousPotentialReplies=len(potentialReplies)
        potentialReplies, replyHits=search_by_usermention_max_id(userMention, twitterSession, potentialReplies, replyHits, rootTweet, language)
    #latest_tweet=potentialReplies[-1].get_id()
    #previousTweetList=0
            # Looping as long we reached the maximum replies or there are no new Tweets
    replyHits=clean_hits(replyHits, max_replies)
    response=create_response(rootTweet.convert_to_new_dict(), convert_list_to_dict(replyHits))            
    return response


# Elli
def get_quote_tweets(twitterSession, tweet, language):
    """
    @param twitterSession: Connection to Twitter-API via Twython needed
    @param rootTweet: Tweet(Object) for which we seek quotes
    @param language: 
    
    @return Updated lists of potentialReplies & replyHits. These are the latest tweets
    
    @desc Calls the first 100 Tweets. They have to be older than related tweet  
    """
    print("___________________________________________")
    print("INFO: LOOKING FOR QUOTE TWEETS OF TWEET", tweet.get_tweet_id(), " (", tweet.get_user_screenname(),")")
    
    quoteTweetHits = []
    
    try:
        newTweets=twitterSession.search(q='https://twitter.com/' + tweet.get_user_screenname() + '/status/' + tweet.get_tweet_id_str() + ' -filter:retweets', count=100, lang=language)
            # (re)construct the tweet URL of the root tweet / tweet for which quote tweets are searched
        if newTweets.get('statuses'):
            for atweet in newTweets['statuses']: # TODO: wie hier diesen Iterator nennen?
                tweetObj=Tweet.Tweet(atweet)
                quoteTweetHits.append(tweetObj)
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
        
    
            # We finally know how many quote tweets the tweet has and so save this information within the TweetObject
    tweet.set_quote_tweet_quantity(len(quoteTweetHits))
    
    
        # Produce some control information shown in the console
    print("INFO: ", len(quoteTweetHits), "QUOTE TWEETS IDENTIFIED")
    if len(quoteTweetHits)!=0:
        print("INFO: FOLLOWING ID's ARE QUOTE TWEETS")
        for hit in quoteTweetHits:
            print("------> ", hit.get_tweet_id())
            

        # TODO: adapt the below comment for the piece of code
        # If the replyHits-list in this instance is not 0, go through the list and call a new instance for every hit. After that,
        # construct a new Dictionary with the tweet and its replies of the current instance. Else, just construct a new Dictionary
        # with the Tweet and set the replies to null.
    if len(quoteTweetHits)!=0:
        quoteTweetList = []
        for hit in quoteTweetHits:
            quoteTweetList.append(get_quote_tweets(twitterSession, hit, language))
            quoteTweets={'1.tweet': tweet.convert_to_new_dict(), '3.quote_tweets':quoteTweetList}   
        return quoteTweets
    else:
        quoteTweets={'1.tweet': tweet.convert_to_new_dict(), '3.quote_tweets':None}
        return quoteTweets



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
                tweetObj=Tweet.Tweet(tweet)
                potentialReplies.append(tweetObj)
                if tweetObj.get_reply_to_tweet_id()==rootTweet.get_tweet_id():
                    replyHits.append(tweetObj)
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
    return potentialReplies, replyHits


def search_by_usermention_max_id(userMention, session, potentialReplies, replyHits, rootTweet, language):
    """ 
    @param userMention: '@user'-String expecting
    @param session: Connection to Twitter-API via Twython needed
    @param potentialReplies: List of all received Tweets(Object) as potential Replies -> needed to always the same 100 Tweets
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
                tweetObj = Tweet.Tweet(tweet)
                potentialReplies.append(tweetObj)
                if tweetObj.get_reply_to_tweet_id()==rootTweet.get_tweet_id():
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
    newTweetObjectList=[]
    for tweetObject in tweetObjectList:
        newTweetObjectList.append(tweetObject.convert_to_new_dict())
    return newTweetObjectList
    
    
      
    
    

    