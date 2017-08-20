# nthcolumn  🔹‏
import mechanize
import cookielib
import time
from random import randint

import os, sys, requests, pattern, json, tweepy
from bs4 import BeautifulSoup

from six.moves.html_parser import HTMLParser

h = HTMLParser() 

from reverend.thomas import Bayes
ai = Bayes()

from hackernews import HackerNews
hn = HackerNews()

#build browser object
br = mechanize.Browser() 
 
# set cookies
cookies = cookielib.LWPCookieJar()
br.set_cookiejar(cookies)
 
# browser settings (used to emulate a browser)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_debug_http(False)
br.set_debug_responses(False)
br.set_debug_redirects(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def getPostIds(nick):
    userl = 'https://hacker-news.firebaseio.com/v0/user/%s.json?print=pretty' % nick
    r = requests.get(userl)
    user = json.loads(r.content)
    return user['submitted']

# reddit
def getReddit(nick, n=100):
    userl = 'https://www.reddit.com/user/%s/comments/.json' % nick
    r = br.open(userl)
    user = json.loads(r.read())
    threads = user['data']['children']
    threads = [thread['data']['body'] for thread in threads]
    return threads[:n]

# hackernews
def getPosts(nick, n=100):
    text = ""
    postIds = getPostIds(nick)
    posts = []
    for id in postIds[:n]:
        post = hn.get_item(id).text or " "
        soup = BeautifulSoup(post, "lxml")
        posts.append(h.unescape(soup.get_text()))
                
    return posts

def getTweets(nick, n=500):
    with open('config.json') as data_file: jsons = json.load(data_file)
    auth = tweepy.OAuthHandler(jsons['twitter']['consumer_key']
                             , jsons['twitter']['consumer_secret'])
    auth.set_access_token(jsons['twitter']['access_token_key']
                        , jsons['twitter']['access_token_secret'])
    api = tweepy.API(auth)
    tweets = api.user_timeline(nick, count=n)
    tweets = [tweet.text.encode("utf-8") for tweet in tweets]
        
    return tweets

nick = 'shalmanese' # hate this guy joosters 
posts = getPosts(nick, n=500)
for post in posts[10:]:
    ai.train(nick, post)

nick = 'th3j35t3r' # hate this guy 
posts = getTweets(nick, n=500)
for post in posts[10:]:
    ai.train(nick, post)
    
nick = 'weev' # hate this guy 
posts = getReddit(nick, n=500)
for post in posts[10:]:
    ai.train(nick, post)
