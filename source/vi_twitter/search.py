'''
Created on 20 Nov 2018

@author: markeschweiler
'''
from vi_twitter.connector import connect_to_api
from vi_twitter.exporter import save_to_json as save
import vi_twitter.TweetObject as Tweet
from _sqlite3 import connect


def search_tweets(keyword):
    twitter_session=connect_to_api()
    tweetList = []
    #get Tweets via API
    tweets = twitter_session.search(q=keyword, count=100, result_type='recent')
    if tweets.get('statuses'):
        for tweet in tweets['statuses']:
            tweetList.append(tweet)
    save(tweetList)
    content = ""
    for t in tweetList:
        tweet_obj=Tweet.Tweet(t)
        next_tweet = tweet_obj.get_timestamp()+" Tweet: "+tweet_obj.get_tweet_content()+"("+tweet_obj.get_user_name()+") \n"
        #next_retweet = tweet_obj.get_retweeted_timestamp()+"Retweeted Tweet:"+tweet_obj.get_retweeted_text()+"("+tweet_obj.get_retweeted_user()+") \n"
        content = content + "\n" + next_tweet# +next_retweet
    return content


def search_retweets_by_id(id):
    twitter_session=connect_to_api()
    tweetList = []
    tweets = twitter_session.get_retweets(id=id)
    for tweet in tweets:
        tweetList.append(tweet)
        print(tweet)
    save(tweetList)
    
    
    content = ""
    for t in tweetList:
        tweet_obj=Tweet.Tweet(t)
        next_tweet = tweet_obj.get_timestamp()+" Tweet: "+tweet_obj.get_tweet_content()+"("+tweet_obj.get_user_name()+") \n"
        next_retweet = tweet_obj.get_retweeted_timestamp()+"Retweeted Tweet:"+tweet_obj.get_retweeted_text()+"("+tweet_obj.get_retweeted_user()+") \n"
        content = content + "\n" + next_tweet + next_retweet
    return content
    

def search_replies_by_id(searched_id):
    twitter_session=connect_to_api()
    tweetList = []
    replyList = []
    searched_tweet = twitter_session.show_status(id=searched_id) 
    print("First Tweet: ",searched_tweet)  
    searched_tweet_obj = Tweet.Tweet(searched_tweet)
    repliedUser=searched_tweet_obj.get_user_screenname()
   
   
    
    for x in range(0, 100):
        tweets = twitter_session.search(q="@"+repliedUser, count=100, result_type='recent', since_id=searched_id)
        if tweets.get('statuses'):
            for tweet in tweets['statuses']:
                
                tweetList.append(tweet)
                if tweet['in_reply_to_status_id']==searched_id:
                    replyList.append(tweet)
                    print("Reply: ",tweet)
        
                    
        lastTweet = Tweet.Tweet(tweetList[-1])
        searched_id=lastTweet.get_tweet_id()
        print("Browsed Tweets:", x*100, "/10.000")
        
    content = content= " Tweet: "+searched_tweet_obj.get_tweet_content()+"( "+searched_tweet_obj.get_user_name()+") \n"
    for reply in replyList:
        reply_obj=Tweet.Tweet(reply)
        print(reply_obj.get_tweet_content())
        content = content + "\n" + " Reply: " + reply_obj.get_tweet_content()+" ("+reply_obj.get_user_name()+") \n"
    
    save(replyList)
    
    return content

def get_user_timeline(uid):
    twitter_session=connect_to_api()
    tweets=twitter_session.get_mentions_timeline(screen_name="spinfocl")
    #tweets=twitter_session.get_user_timeline(user_id=uid)
    print(tweets)
    
    for tweet in tweets:
        print(tweet)
        
    save(tweets)
                
    return "Done"
    
    
def get_replies(tweet_id):
    twitter_session=connect_to_api()
    tweet=twitter_session.show_status(id=tweet_id)
    tweetList=[]
    replyList=[]
    mention="@"+tweet['user']['screen_name']
    print(mention)
    replies=twitter_session.search(q=mention)
    if replies.get('statuses'):
            for reply in replies['statuses']:
                print("Mentions: ", reply['text'])
                tweetList.append(reply)
                if reply['in_reply_to_status_id']==tweet_id:
                    replyList.append(reply)
                    print("Reply To Tweet: ", reply['text'])
    content = "Searched Tweet: "+tweet['text']+" ("+mention+") \n"               
                    
    for reply in replyList:
        content=content+"\n Reply: "+reply['text']+ " ("+reply['user']['screen_name']+") \n"    
    
    
    return content
        

            
   
    
      
    
    

    