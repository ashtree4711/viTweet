'''
Created on 20 Nov 2018

@author: markeschweiler
'''
from vi_twitter.connector import connect_to_api
from vi_twitter.utilities import save_to_json as save, save_response_json
import vi_twitter.TweetObject as Tweet
import twython



    # Workaround Function  
def get_replies(tweet_id, max_replies):
    twitterSession = connect_to_api() 
    potentialReplies=[]
    replyHits= []
    previousPotentialReplies=0
    rootTweet = get_root_tweet_by_id(tweet_id, twitterSession)
        # create from the screenname a user mention
    userMention="@"+rootTweet.get_user_screenname()+"-filter:retweets"
 
        # First Round: We need the parameter "since_id" first, because the API will give us automatically the latest tweets
        #              and we just have to take care, that no Tweet should be older than the Root Tweet.
    potentialReplies, replyHits=search_by_usermention_since_id(userMention, twitterSession, potentialReplies, replyHits, rootTweet)
        # Second Round: Now, we need the max_id since the every call to API will give us, as already said, the latest tweet.
        #               So we do need Tweets, which are older than the already received Tweets. We get them, if we take the last
        #               Tweet of the existing list and declare it as the max_id.
    while (len(replyHits) <= max_replies and previousPotentialReplies < len(potentialReplies) and potentialReplies[-1].get_tweet_id() > rootTweet.get_tweet_id()):
        previousPotentialReplies=len(potentialReplies)
        potentialReplies, replyHits=search_by_usermention_max_id(userMention, twitterSession, potentialReplies, replyHits, rootTweet)
        print("___________________________________________")
        print("FOUND REPLIES: ", len(replyHits))
    #latest_tweet=potentialReplies[-1].get_id()
    #previousTweetList=0
            # Looping as long we reached the maximum replies or there are no new Tweets
    replyHits=clean_hits(replyHits, max_replies)
    
        
           
    save_response_json(rootTweet.convert_to_new_dict(), convert_list_to_dict(replyHits))    
       
    content = "Searched Tweet: "+rootTweet.get_tweet_content()+" ("+userMention+") \n"               
            # Temporary constructs a string to shown on localhost :-P               
    for reply in replyHits:
        content=content+"\n Reply: "+reply.get_tweet_content()+ " ("+reply.get_user_screenname()+") \n"    
    return content

def get_root_tweet_by_id(tweet_id, session):
    rootTweet = session.show_status(id=tweet_id)
    rootTweet = Tweet.Tweet(rootTweet)
    return rootTweet

def search_by_usermention_since_id(userMention, session, potentialReplies, replyHits, rootTweet):
    '''
        Used for the first 100 Tweets.
        
        # userMention: '@user'-String expecting
        # session: Connection to Twitter-API via Twython needed
        # potentialReplies: List of all received Tweets(Object) as potential Replies -> needed to always the same 100 Tweets
        # replyHits: List of all hitted Reply-Tweets(Object)
        # rootTweet: Tweet(Object) for which we seek replies 
        # return: Updated lists of potentialReplies & replyHits
    '''
    try:
        print("______________________________________________________________________________________________________________")
        newTweets=session.search(q=userMention, count=100, result_type='recent', since_id=rootTweet.get_tweet_id())
        if newTweets.get('statuses'):
            for tweet in newTweets['statuses']:
                tweetObj=Tweet.Tweet(tweet)
                print(tweetObj.get_timestamp(), "[", tweetObj.get_tweet_id_str(), "] Mentions: ", tweetObj.get_tweet_content())
                potentialReplies.append(tweetObj)
                if tweetObj.get_reply_to_tweet_id()==rootTweet.get_tweet_id():
                    replyHits.append(tweetObj)
                    print("REPLY FOUND")
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
    return potentialReplies, replyHits


def search_by_usermention_max_id(userMention, session, potentialReplies, replyHits, rootTweet):
    '''
        Used for the 100+ Tweets.
        
        # userMention: '@user'-String expecting
        # session: Connection to Twitter-API via Twython needed
        # potentialReplies: List of all received Tweets(Object) as potential Replies -> needed to always the same 100 Tweets
        # replyHits: List of all hitted Reply-Tweets(Object)
        # rootTweet: Tweet(Object) for which we seek replies 
        # return: Updated lists of potentialReplies & replyHits
    '''
    try:
        print("______________________________________________________________________________________________________________")
        newTweets=session.search(q=userMention, count=100, result_type='recent', max_id=potentialReplies[-1].get_tweet_id()-1)
        if newTweets.get('statuses'):
            for tweet in newTweets['statuses']:
                tweetObj = Tweet.Tweet(tweet)
                    # Just for control!
                print(tweetObj.get_timestamp(), "[", tweetObj.get_tweet_id_str(), "] Mentions: ", tweetObj.get_tweet_content())
                potentialReplies.append(tweetObj)
                if tweetObj.get_reply_to_tweet_id()==rootTweet.get_tweet_id():
                    replyHits.append(tweetObj)
                    print("REPLY FOUND")        
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
    return potentialReplies, replyHits
   
def clean_hits(replyHits, max_replies):
    newReplyHits=[]
    for reply in replyHits[0:max_replies]:
        newReplyHits.append(reply)
    return newReplyHits

def convert_list_to_dict(tweetObjectList):
    newTweetObjectList=[]
    for tweetObject in tweetObjectList:
        newTweetObjectList.append(tweetObject.convert_to_new_dict())
    return newTweetObjectList
            
    
    
    
      
    
    

    