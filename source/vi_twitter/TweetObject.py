"""
With TweetObject.py we construct a Tweet object for each Tweet and initiate it with selected attributes of the Tweet
"""

class Tweet(object):
    """
        The 'Tweet' class is viTweet's own object class consisting of the useful attributes of the tweets provided by the 
        Twitter API. All attributes are callable via setters and getters
    """


    def __init__(self, api_json):
        """
          @param api_json: The Tweet-Information from Twitter
          
          @desc We construct for every useful information an attribute within an object  
        """
        # General Information of posted Tweet
        self.timestamp = api_json['created_at'] # String
        self.tweet_id = int(api_json['id']) # Integer
        self.tweet_id_str= api_json['id_str'] # String
        self.tweet_content = api_json['text'] # String
        
        # Information about User of posted Tweet
        self.user = api_json['user'] # List
        self.user_id = api_json['user']['id'] # Integer
        self.user_name = api_json['user']['name'] # String
        self.user_screenname = api_json['user']['screen_name'] # String
        self.user_location = api_json['user']['location'] # String
        self.user_url = api_json['user']['url'] # String
        self.user_desc = api_json['user']['description'] # String
        
        # Geo-Location of Tweet -> https://developer.vi_twitter.com/en/docs/geo/place-information/api-reference/get-geo-id-place_id.html
        
        # Entities of a Tweet (Hashtags, User-Mentions, Media) -> https://developer.vi_twitter.com/en/docs/tweets/data-dictionary/overview/entities-object.html
        # Reply / Quoted Tweets Information
        self.reply_to_tweet_id = api_json['in_reply_to_status_id'] # Integer
        self.reply_to_tweet_id_str = api_json['in_reply_to_status_id_str'] # String
        self.reply_to_user_id = api_json['in_reply_to_user_id'] # Integer
        self.reply_to_user_id_str = api_json['in_reply_to_user_id_str'] # String
        self.reply_isQuote = api_json['is_quote_status']  # Boolean
        if api_json['is_quote_status']:
            self.quote_to_tweet_id = api_json['quoted_status_id'] # Integer
            self.quote_to_tweet_id_str = api_json['quoted_status_id_str'] #String
        else:
            self.quote_to_tweet_id = None # Integer
            self.quote_to_tweet_id_str = None #String
        self.reply_quantity = 0 # Integer
        self.quote_tweet_quantity = 0 # Integer
        
        
        # List with refering Tweet-ID
        self.replied_by_list = [] # Array
        self.quoted_by_list = [] # Array
        
        # Embedded Tweet
        self.embedded_tweet = self.create_embedded_tweet() # String
        
        
        # Retweet
        if 'retweeted_status' in api_json.keys():
            self.retweet_count = api_json['retweet_count'] # Integer
            self.retweeted_timestamp = api_json['retweeted_status']['created_at'] # String
            self.retweeted_text = api_json['retweeted_status']['text'] # String
            self.retweeted_user = api_json['retweeted_status']['user']['name'] #String
            
        self.convertedDict = self.convert_to_new_dict()

    
    def create_embedded_tweet(self):
            # Constructs html-blockquote and Script to create a embeddeed tweet
        blockquote_start = "<blockquote class='twitter-tweet' data-lang='de' data-conversation='none' data-width='400' data-align='center'>"
        content = "<p dir='ltr'>"+self.tweet_content+"</p>"
        user = "&mdash; "+self.user_name+" (@"+self.user_screenname+") "
        link = "<a href='https://twitter.com/"+self.user_screenname+"/status/"+self.tweet_id_str+"?ref_src=twsrc%5Etfw'>"
        time = self.timestamp
        blockquote_end = "</a></blockquote><script async src='https://platform.twitter.com/widgets.js' charset='utf-8'></script>"
        self.embedded_tweet = blockquote_start+content+user+link+time+blockquote_end
        #print(self.embedded_tweet)
        return self.embedded_tweet
    
    def get_embeddeed_tweet(self):
        return self.embedded_tweet
    
    def get_converted_structure(self):
        return self.__convertedTweetStructure
    
    def convert_to_new_dict(self):
        """
            @desc Here we construct a new reduced Tweet-Dictionary with the Information we possible need.
        """
        new_dict = {'timestamp': self.timestamp,'tweet_id':self.tweet_id, 'tweet_content':self.tweet_content, 'reply_to':self.reply_to_tweet_id, 'quote_to':self.quote_to_tweet_id, 'number_of_replies':self.reply_quantity, 'replied_by':self.get_replied_by_list(), 'isQuote': self.reply_isQuote ,'number_of_quote_tweets':self.quote_tweet_quantity, 'quoted_by':self.get_quoted_by_list(),'embeddingCode':self.embedded_tweet,
                     'user':{'user_id':self.user_id, 'user_name':self.user_name, 'screen_name':self.user_screenname,
                            'location':self.user_location, 'description': self.user_desc}}
        
        return new_dict
    
    
        
    def get_converted_dict(self):
        return self.convertedDict   
    
    
    def get_timestamp(self):
        return self.__timestamp


    def get_tweet_id(self):
        return self.__tweet_id


    def get_tweet_id_str(self):
        return self.__tweet_id_str


    def get_tweet_content(self):
        return self.__tweet_content


    def get_user(self):
        return self.__user


    def get_user_id(self):
        return self.__user_id


    def get_user_name(self):
        return self.__user_name


    def get_user_screenname(self):
        return self.__user_screenname


    def get_user_location(self):
        return self.__user_location


    def get_user_url(self):
        return self.__user_url


    def get_user_desc(self):
        return self.__user_desc


    def get_reply_to_tweet_id(self):
        return self.__reply_to_tweet_id


    def get_reply_to_tweet_id_str(self):
        return self.__reply_to_tweet_id_str


    def get_reply_to_user_id(self):
        return self.__reply_to_user_id


    def get_reply_to_user_id_str(self):
        return self.__reply_to_user_id_str


    def get_reply_is_quote(self):
        return self.__reply_isQuote
    
    def get_reply_quantity(self):
        return self.reply_quantity 
    
    def get_quote_to_tweet_id(self):
        return self.quote_to_tweet_id 
    
    def get_quote_to_tweet_id_str(self):
        return self.quote_to_tweet_id_str   
    
    def get_quote_tweet_quantity(self):
        return self.quote_tweet_quantity
    

    def get_retweet_count(self):
        return self.__retweet_count


    def get_retweeted_timestamp(self):
        return self.__retweeted_timestamp


    def get_retweeted_text(self):
        return self.__retweeted_text


    def get_retweeted_user(self):
        return self.__retweeted_user
    
    def get_replied_by_list(self):
        return self.replied_by_list
    
    def get_quoted_by_list(self):
        return self.quoted_by_list

    def set_timestamp(self, value):
        self.__timestamp = value


    def set_tweet_id(self, value):
        self.__tweet_id = value


    def set_tweet_id_str(self, value):
        self.__tweet_id_str = value


    def set_tweet_content(self, value):
        self.__tweet_content = value


    def set_user(self, value):
        self.__user = value


    def set_user_id(self, value):
        self.__user_id = value


    def set_user_name(self, value):
        self.__user_name = value


    def set_user_screenname(self, value):
        self.__user_screenname = value


    def set_user_location(self, value):
        self.__user_location = value


    def set_user_url(self, value):
        self.__user_url = value


    def set_user_desc(self, value):
        self.__user_desc = value


    def set_reply_to_tweet_id(self, value):
        self.__reply_to_tweet_id = value


    def set_reply_to_tweet_id_str(self, value):
        self.__reply_to_tweet_id_str = value


    def set_reply_to_user_id(self, value):
        self.__reply_to_user_id = value


    def set_reply_to_user_id_str(self, value):
        self.__reply_to_user_id_str = value


    def set_reply_is_quote(self, value):
        self.__reply_isQuote = value
        
    def set_quote_to_tweet_id(self, value):
        self.__quote_to_tweet_id = value
    
    def set_quote_to_tweet_id_str(self, value):
        self.__quote_to_tweet_id_str = value 
        
    def set_reply_quantity(self, value):
        self.reply_quantity = value
        
    def set_quote_tweet_quantity(self, value):
        self.quote_tweet_quantity = value

    def set_retweet_count(self, value):
        self.__retweet_count = value
        
    def raise_reply_quantity(self):
        self.reply_quantity = self.reply_quantity+1
        
    def raise_quote_tweet_quantity(self):
        self.quote_tweet_quantity = self.quote_tweet_quantity+1


    def set_retweeted_timestamp(self, value):
        self.__retweeted_timestamp = value


    def set_retweeted_text(self, value):
        self.__retweeted_text = value


    def set_retweeted_user(self, value):
        self.__retweeted_user = value
        
    def set_replied_by_list(self, value):
        self.replied_by_list.append(value)
    
    def set_quoted_by_list(self, value):
        self.quoted_by_list.append(value)


    def del_timestamp(self):
        del self.__timestamp


    def del_tweet_id(self):
        del self.__tweet_id


    def del_tweet_id_str(self):
        del self.__tweet_id_str


    def del_tweet_content(self):
        del self.__tweet_content


    def del_user(self):
        del self.__user


    def del_user_id(self):
        del self.__user_id


    def del_user_name(self):
        del self.__user_name


    def del_user_screenname(self):
        del self.__user_screenname


    def del_user_location(self):
        del self.__user_location


    def del_user_url(self):
        del self.__user_url


    def del_user_desc(self):
        del self.__user_desc


    def del_reply_to_tweet_id(self):
        del self.__reply_to_tweet_id


    def del_reply_to_tweet_id_str(self):
        del self.__reply_to_tweet_id_str


    def del_reply_to_user_id(self):
        del self.__reply_to_user_id


    def del_reply_to_user_id_str(self):
        del self.__reply_to_user_id_str


    def del_reply_is_quote(self):
        del self.__reply_isQuote


    def del_retweet_count(self):
        del self.__retweet_count


    def del_retweeted_timestamp(self):
        del self.__retweeted_timestamp


    def del_retweeted_text(self):
        del self.__retweeted_text


    def del_retweeted_user(self):
        del self.__retweeted_user

    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
    tweet_id = property(get_tweet_id, set_tweet_id, del_tweet_id, "tweet_id's docstring")
    tweet_id_str = property(get_tweet_id_str, set_tweet_id_str, del_tweet_id_str, "tweet_id_str's docstring")
    tweet_content = property(get_tweet_content, set_tweet_content, del_tweet_content, "tweet_content's docstring")
    user = property(get_user, set_user, del_user, "user's docstring")
    user_id = property(get_user_id, set_user_id, del_user_id, "user_id's docstring")
    user_name = property(get_user_name, set_user_name, del_user_name, "user_name's docstring")
    user_screenname = property(get_user_screenname, set_user_screenname, del_user_screenname, "user_screenname's docstring")
    user_location = property(get_user_location, set_user_location, del_user_location, "user_location's docstring")
    user_url = property(get_user_url, set_user_url, del_user_url, "user_url's docstring")
    user_desc = property(get_user_desc, set_user_desc, del_user_desc, "user_desc's docstring")
    reply_to_tweet_id = property(get_reply_to_tweet_id, set_reply_to_tweet_id, del_reply_to_tweet_id, "reply_to_tweet_id's docstring")
    reply_to_tweet_id_str = property(get_reply_to_tweet_id_str, set_reply_to_tweet_id_str, del_reply_to_tweet_id_str, "reply_to_tweet_id_str's docstring")
    reply_to_user_id = property(get_reply_to_user_id, set_reply_to_user_id, del_reply_to_user_id, "reply_to_user_id's docstring")
    reply_to_user_id_str = property(get_reply_to_user_id_str, set_reply_to_user_id_str, del_reply_to_user_id_str, "reply_to_user_id_str's docstring")
    reply_isQuote = property(get_reply_is_quote, set_reply_is_quote, del_reply_is_quote, "reply_isQuote's docstring")
    retweet_count = property(get_retweet_count, set_retweet_count, del_retweet_count, "retweet_count's docstring")
    retweeted_timestamp = property(get_retweeted_timestamp, set_retweeted_timestamp, del_retweeted_timestamp, "retweeted_timestamp's docstring")
    retweeted_text = property(get_retweeted_text, set_retweeted_text, del_retweeted_text, "retweeted_text's docstring")
    retweeted_user = property(get_retweeted_user, set_retweeted_user, del_retweeted_user, "retweeted_user's docstring")

