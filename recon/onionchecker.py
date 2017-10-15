# onionchecker
import requests
import json
import re

regex = re.compile("<title>(.*?)</title>")

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

# top onion sites
with open("toptor.txt") as infile: 
    urls = infile.read().split('\n')

for url in urls:
    try:
        # knock
        response = requests.get(url,proxies=proxies,timeout=10)
        if response.status_code == 200:
            title = regex.findall(response.content)[0]
            with open("darkwebdir.csv", 'a') as outfile:
                outfile.write("%s ~ %s\n" % (url, title)) 
            print "Found     :: %s ~ %s" % (urn, title)
            
        # progress
        if urls.index(url) % 1000 == 0:
            print "Processed :: %s" % url
    except:
        print "Tried      :: %s" % url
        
