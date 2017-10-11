import requests, re
from itertools import permutations
from string import ascii_lowercase, digits
  
characters = digits + ascii_lowercase + '-_'
for x in permutations(characters, 3):
    word = ''.join(x)
    url = 'http://%s.s3.amazonaws.com/' % word
    try:
        response = requests.head(url)
        if response.status_code == 200: 
            sample = requests.get(url).content
            matches = re.findall(r'<Key>(\s*(.*(zip|pem|sql|csv|xls|tgz|dmp|rsa|tok|tar|bak|p12)))(?=\n</Key)', sample)
            for match in matches:
                print 'http://%s.s3.amazonaws.com/%s' % (word, match[1])
    except:
        print word
        
