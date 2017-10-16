import requests, re
from bs4 import BeautifulSoup
from itertools import permutations
from string import ascii_lowercase, digits

# find buckets with files with these  
regex = re.compile("(\.zip|\.pem|\.sql|\.csv|\.xls|\.doc)", re.I)

# all 100k top domain names
with open("topdoms.txt") as infile: 
  urls = infile.read().split('\n')

# all 370k top words
with open("words.txt") as infile: 
  urls = infile.read().split('\n')

# all four character words
characters = digits + ascii_lowercase #+ '.-_'
urls += [''.join(chars) for chars in permutations(characters, 4)]

for url in urls:
    try:
        # knock
        full = 'http://%s.s3.amazonaws.com/' % url
        response = requests.head(full)
        if response.status_code == 200:
            with open("cache.csv", 'a') as outfile:
                outfile.write(full) 
            # enter
            response = requests.get(full)
            soup = BeautifulSoup(response.content, "lxml")
            matches = soup.find_all('key', text=regex)
            for match in matches:
                path = match.text
                urn = "%s%s" % (full, match.text)
                with open("results.html", 'a') as outfile:
                    outfile.write('<a href="%s">%s</a>\n' % (urn,path))
                # auto download feature
                # response = requests.get(urn)
                print "Matched   :: %s" % urn
        # progress
        if urls.index(url) % 1000 == 0:
            print "Processed :: %s" % url
    except:
        print "Tried    :: %s" % url
