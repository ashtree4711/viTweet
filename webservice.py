'''
Created on 16 Nov 2018
'import urlparse'
@author: markeschweiler
'''
import os
import redis


from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.wrappers import Response, Request
from jinja2 import Environment, FileSystemLoader
from twython.api import Twython
from viTweet import twitter_api as api
from viTweet import tweet





class WebService(object):

    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='new_url'),
            Rule('/<short_id>', endpoint='follow_short_link'),
            Rule('/<short_id>+', endpoint='short_link_details')])
        

    def dispatch_request(self, request):
        'tweets = api.search_tweets("trump")'
        tweets = api.search_retweets_by_id()
        content = ""
        for t in tweets:
            tweet_obj=tweet.Tweet(t)
            next_tweet = tweet_obj.get_timestamp()+" Tweet: "+tweet_obj.get_tweet_content()+"("+tweet_obj.get_user_name()+") \n"
            next_retweet = tweet_obj.get_retweeted_timestamp()+"Retweeted Tweet:"+tweet_obj.get_retweeted_text()+"("+tweet_obj.get_retweeted_user()+") \n"
            content = content + "\n" + next_tweet +next_retweet

        
        
        
           
            
            
    
        return Response(content)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
    
 

    
def render_template(self, template_name, **context):
    t = self.jinja_env.get_template(template_name)
    return Response(t.render(context), mimetype='text/html')


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = WebService({
        'redis_host':       redis_host,
        'redis_port':       redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

