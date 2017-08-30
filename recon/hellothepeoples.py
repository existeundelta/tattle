import requests
import tweepy
import json
import time
from bs4 import BeautifulSoup
import os

os.chdir('/home/dad/Documents/tattle/')
with open('config.json') as data_file: 
    jsons = json.load(data_file)
    auth = tweepy.OAuthHandler(jsons['twitter']['consumer_key'], jsons['twitter']['consumer_secret'])
    auth.set_access_token(jsons['twitter']['access_token_key'], jsons['twitter']['access_token_secret'])
    api = tweepy.API(auth)

url = 'https://steemit.com/@theshadowbrokers'

Zzz = 1800
while True:
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        post = soup.h3.a.text
        if not post == u'TheShadowBrokers Monthly Dump Service - August 2017':
            api.update_status(post[:140])
            break        
        time.sleep(Zzz)
    except Exception as error:
        print error.message
    

