import re
import sqlite3
import time

from bs4 import BeautifulSoup
from requests import get as GET
   
def read():
    latest = GET('http://pastebin.com/archive').content
    soup = BeautifulSoup(latest, "lxml")
    table = soup.select('table.maintable')
    links = table[0].findAll('a')
    urls = [link['href'] for link in links if len(link['href'])<10]
    return urls

def save(params):
    db = sqlite3.connect('bar.db')
    db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    sql = db.cursor()
    if type(params) is list:
        sql.executemany("INSERT INTO paste VALUES (?,?,?)", params)
    else:
        sql.execute("INSERT INTO paste VALUES (?,?,?)", params)
    db.commit()
    db.close()

def show():
    db = sqlite3.connect('bar.db')
    sql = db.cursor()    
    for row in sql.execute("SELECT * FROM paste"):
        print row
    db.close()

def kill():
    db = sqlite3.connect('bar.db')
    sql = db.cursor()    
    for row in sql.execute("DELETE FROM paste"):
        print row
    db.commit()
    db.close()

passwords = [':admin', ':1234', 'xc3511', 'GMB182', 'Zte521', 'vizxv', 'oelinux123', 'jauntech']
passwords = "(.*" + ".*)|(.*".join(passwords) + ".*)"

justOnce = True

Zzz = 240
while True:
    try:
        pois = []
        urls = read()
        for url in urls:
            file = 'https://pastebin.com/raw%s' % url
            print file
            text = GET(file).content
            
            # check for email addresses
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
            if len(emails) > 20:
                print 'Email addresses'
                pois.append((file, 'email', text.encode('UTF-8'),))
                continue
                
            # check for ip addresses followed by a port
            found = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}:)',text)
            if len(found) > 20:
                print 'IP addresses'
                pois.append((file, 'IP', text,))
                continue
                
            # check for admins
            pwned = re.findall(passwords,text)   
            if pwned:
                print 'Admin passwords'
                pois.append((file, 'pwned', text,))
                continue
                
            # check for keys
            keys = re.findall('.*-----BEGIN (RSA|DSA) PRIVATE KEY-----.*',text)   
            if keys:
                print 'Private keys'
                pois.append((file, 'keys', text,))
                continue
                        
        if len(pois): save(pois)
        print 'Checking again in %s minutes' % (Zzz/60)
        time.sleep(Zzz)        
    except Exception as error:
        print error.message
        
    if justOnce: break
    