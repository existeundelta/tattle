# nthcolumn 
import mechanize
import cookielib
import time
import os, sys, requests, pattern, json, tweepy
import numpy as np

from random import randint
from pattern.en import sentiment
from bs4 import BeautifulSoup

from six.moves.html_parser import HTMLParser
h = HTMLParser()

from reverend.thomas import Bayes
ai = Bayes()

from hackernews import HackerNews
hn = HackerNews()
    
# pastebin
def getPasteURLs():
    pastebin = 'http://pastebin.com/archive'
    latest = requests.get(pastebin).content
    soup = BeautifulSoup(latest, "lxml")
    table = soup.select('table.maintable')
    links = table[0].findAll('a')
    urls = [link['href'] for link in links if len(link['href'])<10]
    return urls

# reddit
def getReddit(nick, n=100):
    userl = 'https://www.reddit.com/user/%s/comments/.json' % nick
    r = br.open(userl)
    user = json.loads(r.read())
    threads = user['data']['children']
    threads = [thread['data']['body'] for thread in threads]
    return threads[:n]

# hackernews
def getPostIds(nick):
    userl = 'https://hacker-news.firebaseio.com/v0/user/%s.json?print=pretty' % nick
    r = requests.get(userl)
    user = json.loads(r.content)
    return user['submitted']

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
    with open('config.json') as data_file: settings = json.load(data_file)
    auth = tweepy.OAuthHandler(settings['twitter']['consumer_key']
                             , settings['twitter']['consumer_secret'])
    auth.set_access_token(settings['twitter']['access_token_key']
                        , settings['twitter']['access_token_secret'])
    api = tweepy.API(auth)
    tweets = api.user_timeline(nick, count=n)
    tweets = [tweet.text.encode("utf-8") if tweet.author.screen_name == nick else None for tweet in tweets]
    return tweets

def geo_mean(iterable):
    a = np.array(iterable)
    if len(a): 
        return a.prod()**(1.0/len(a))

# average geometric mean polarity/subjectivity
def meanness(posts, type=0):
    T1, T2, N3 = [], [], 0
    for post in posts:
        try:
            post = post.decode('utf-8',errors='ignore')
        except Exception as error:
            print post, error.message
            pass
        scores = sentiment(post)
        point = scores[type]
        if (point > 0):
            T1.append(point)
        elif (point < 0):
            T2.append(abs(point))
        elif (point == 0):
            N3 += 1
        else:
            pass
    
    N1 = len(T1)
    N2 = len(T2)
    G1 = geo_mean(T1)
    G2 = geo_mean(T2)
    N = N1+N2+N3
    AGM = (N1*G1 - N2*G2)/N    
    return AGM

# reduce(lambda x, y: x*y, numbers)**(1.0/len(numbers))

nick = 'nthcolumn'
posts = getPosts(nick, n=500)
for post in posts[10:]:
    with open('./corpora/%s.txt' % nick, 'a') as file: text = file.write(post+os.linesep)
    ai.train(nick, post)


for post in posts:
    with open('./corpora/%s.txt' % nick, 'a') as file: 
        post = post.encode('ascii','ignore')
        if post:
            text = file.write(post+os.linesep)

def countfeature(posts, feature):
    total = 0
    for post in posts:
        count = post.count(feature)
        total += int(count)
    
    # this gives us our final metrics
    z = len(posts)
    average = float(total) / z
    
    print
    print
    print "Average : ", average
    print "Total: ", total
    
def getFirefox():
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
    
    return br

with open('./corpora/sense.txt') as file: text = file.read()
posts = text.replace('\n','').split('.')

# neat way of ripping grams 
# gramlist = [sentence[i:i+N] for i in xrange(len(sentence)-N+1)]

"""

MalcolmNance = getTweets('MalcolmNance', n=1000)
for post in MalcolmNance[5:]:
    ai.train('MalcolmNance', post)

th3j35t3r = getTweets('th3j35t3r', n=1000)
for post in th3j35t3r[5:]:
    ai.train('th3j35t3r', post)

aroliso = getTweets('aroliso', n=1000)
for post in aroliso[5:]:
    ai.train('aroliso', post)

nick = 'weev'
posts = getReddit(nick, n=500)
for post in posts[10:]:
    ai.train(nick, post)

nick = 'shalmanese' #
posts = getPosts(nick, n=500)
for post in posts[10:]:
    ai.train(nick, post)

"""
