import os, sys
os.chdir('/home/docs/tattle/recon')

import sqlite3
sql = sqlite3.connect('results')
cursor = sql.cursor()
cursor.execute('create table bucket( id INTEGER PRIMARY KEY, base TEXT, url TEXT, name TEXT, size INTEGER)')
cursor.commit()

with open("results.html.csv") as infile: lines = infile.read().split('\n')

template = "REPLACE INTO bucket VALUES(%s,'%s','%s',%s)"



conn = sqlite3.connect('results')
sql.commit()
#cursor.execute("insert into bucket( id, url, name) values (%s, '%s', '%s')" % (urls.index, )
len(urls)
len(lines)
urls = [url.split(',') for url in lines]
len(urls)
urls[0]
urls[100]
for url in urls:
#cursor.execute("insert into bucket( id, url, name) values (%s, '%s', '%s')" % (urls.index, )
dd
url = urls[100]
urls.index(url)
for url in urls:
    cursor.execute("insert into bucket( id, url, name) values (%s, '%s', '%s')" % (urls.index(url), url[0], url[1]))
    sql.commit()

url[6922]
urls[6922]
    cursor.execute("insert into bucket( id, url, name) values (%s, '%s', '%s')" % (urls.index(url), url[0], url[1]))
print("insert into bucket( id, url, name) values (%s, '%s', '%s')" % (urls.index(url), url[0], url[1]))
with open("results.html.csv") as infile: lines = infile.read().split('\n')
urls = [url.split(',') for url in lines]
with open("results.html.csv") as infile: lines = infile.read().split('\n')
len(lines)
len(lines)
urls = [url.split(',') for url in lines]
for url in urls:
    cursor.execute("insert into bucket( id, url, name) values (%s, '%s', '%s')" % (urls.index(url), url[0], url[1]))
    sql.commit()

import os, sys
os.chdir('/home/docs/tattle/recon')
import os, sys
os.chdir('/home/docs/tattle/recon')

with open("results.html.csv") as infile: lines = infile.read().split('\n')

lines
lines[22]
urls = list(set(urls))
urls = list(set(lines))
len(lines)
len(urls)
len(urls)
urls = [url.split(',') for url in lines]
import sqlite3
sql = sqlite3.open('results')
sql = sqlite3.connect('results')
cursor = sql.cursor()
for url in urls:
    print "REPLACE INTO bucket VALUES(%s,'%s','%s',%s)" % (urls.index(url), url[0], url[1])

for url in urls:
    print "REPLACE INTO bucket VALUES(%s,'%s','%s')" % (urls.index(url), url[0], url[1])
