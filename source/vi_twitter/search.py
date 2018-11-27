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
    twitter_session=connect_to_api()
        # get the searched Tweet
    tweet=twitter_session.show_status(id=tweet_id)
    convertedMainTweet = Tweet.Tweet(tweet).get_converted_dict()
    tweetList=[]
    replyList=[]
    convertedReplyList=[]
        # create from the Screenname a Keyword
    mention="@"+tweet['user']['screen_name']+"-filter:retweets"
        # latest_tweet is needed for the loop, because without it, you'll get always the same 100 Tweets
    try:
            # First Round: We need the parameter "since_id" first, because the API will give us automatically the latest tweets
            #              and we just have to take care, that no Tweet should be older than the Root Tweet.
        potential_replies=twitter_session.search(q=mention, count=2, result_type='recent', since_id=tweet_id)
        if potential_replies.get('statuses'):
            for reply in potential_replies['statuses']:
                    # Just for control!
                print(reply['created_at'], "[", reply['id_str'], "] Mentions: ", reply['text'])
                tweetList.append(reply)
                    # Checks all the Tweets with @user, if there is a tweet, which is a reply to the focused tweet
                    # Needs to be converted into a Twitter-Object
                if reply['in_reply_to_status_id']==tweet_id:
                    convertedReply = Tweet.Tweet(reply).get_converted_dict()
                    
                    convertedReplyList.append(convertedReply)
                    replyList.append(reply)
                    
                    print(reply['created_at'], "[", reply['id_str'],"] Reply To Tweet: ", reply['text'])
                
                 
        print("Crawled Mentions: "+tweetList.__len__().__str__()+ "| Found Replies: "+replyList.__len__().__str__())
        
            # Second Round: Now, we need the max_id since the every call to API will give us, as already said, the latest tweet.
            #               So we do need Tweets, which are older than the already received Tweets. We get them, if we take the last
            #               Tweet of the existing list and declare it as the max_id.
        latest_tweet=tweetList[-1]['id']
        previousTweetList=0
            # Looping as long we reached the maximum replies or there are no new Tweets
        while (len(replyList) <= max_replies and previousTweetList < len(tweetList) and tweetList[-1]['id']>tweet_id):
            print("______________________________________________________________________________________________________________")
                # you can change result_type between 'recent', 'popular', 'mixed'
                # since_id searched since a specific tweet. It is needed to get the next 100 tweets and not the same.
            previousTweetList=len(tweetList)
            potential_replies=twitter_session.search(q=mention, count=100, result_type='recent', max_id=latest_tweet-1)
            if potential_replies==None:
                break
            
            if potential_replies.get('statuses'):
                for reply in potential_replies['statuses']:
                        # Just for control!
                    print(reply['created_at'], "[", reply['id_str'], "] Mentions: ", reply['text'])
                    tweetList.append(reply)
                    
                        # Checks all the Tweets with @user, if there is a tweet, which is a reply to the focused tweet
                        # Needs to be converted into a Twitter-Object
                    if reply['in_reply_to_status_id']==tweet_id:
                        convertedReply = Tweet.Tweet(reply).get_converted_dict()
                        convertedReplyList.append(convertedReply)
                        replyList.append(reply)
                        print(reply['created_at'], "[", reply['id_str'],"] Reply To Tweet: ", reply['text'])
                        
                    if replyList.__len__() == max_replies:
                        print("Crawled Mentions: "+tweetList.__len__().__str__()+ "| Found Replies: "+replyList.__len__().__str__())
                        break
                if replyList.__len__() == max_replies:
                    print("Crawled Mentions: "+tweetList.__len__().__str__()+ "| Found Replies: "+replyList.__len__().__str__())
                    break
                     
            print("Crawled Mentions: "+tweetList.__len__().__str__()+ "| Found Replies: "+replyList.__len__().__str__())
            
            latest_tweet=tweetList[-1]['id']
            
    except twython.exceptions.TwythonRateLimitError:
        print("... ATTENTION: Twitter only allows a limited number of requests. Please wait a few minutes.")
            
    save_response_json(convertedMainTweet, convertedReplyList)    
        
    content = "Searched Tweet: "+tweet['text']+" ("+mention+") \n"               
        # Temporary constructs a string to shown on localhost :-P               
    for reply in replyList:
        content=content+"\n Reply: "+reply['text']+ " ("+reply['user']['screen_name']+") \n"    
    return content
        

            
   
      
    
    

    