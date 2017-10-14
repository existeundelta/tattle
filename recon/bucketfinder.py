import requests, re
from bs4 import BeautifulSoup
from itertools import permutations
from string import ascii_lowercase, digits

regex = re.compile("(\.zip|\.pem|\.sql|\.csv|\.xls|\.doc)", re.I)

with open("topdoms.txt") as infile: 
  urls = infile.read().split('\n')

with open("results.html", 'w') as outfile:
    for url in urls:
        try:
            full = 'http://%s.s3.amazonaws.com/' % url
            sample = requests.get(full).content
            soup = BeautifulSoup(sample, "lxml")
            matches = soup.find_all('key', text=regex)
            for match in matches:
                path = match.text
                outfile.write('<a href="%s%s">%s</a>\n' % (full,path,path))
                print "%s%s" % (full, match.text)
        except:
            print url 

characters = digits + ascii_lowercase + '.-_'
for x in permutations(characters, 3):
    url = ''.join(x) 
    try:
        full = 'http://%s.s3.amazonaws.com/' % url
        sample = requests.get(full).content
        soup = BeautifulSoup(sample, "lxml")
        matches = soup.find_all('key', text=regex)
        for match in matches:
            path = match.text
            with open("results.html", 'a') as outfile:
                outfile.write('<a href="%s%s">%s</a>\n' % (full,path,path))
            print "%s%s" % (full, match.text)
    except:
        print url 

