import requests
import tweepy
import json
import time
from bs4 import BeautifulSoup
import shodan

with open('./Documents/tattle/config.json') as data_file: jsons = json.load(data_file)
api = shodan.Shodan(jsons['shodan']['api_key'])

url = 'https://www.bugcrowd.com/bug-bounty-list/'
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")
links = soup.select('#bounty-list > table > tbody > tr > td > a')
for link in links:
    org = link.getText()
    print org
    
    try:
        # Search Shodan
        results = api.search('org:%s' % org)

        # Show the results
        print 'Results found: %s' % results['total']
        for result in results['matches']:
            print 'IP: %s' % result['ip_str']
            print result['data']
            
    except shodan.APIError, e:
        print 'Error: %s' % e
    
