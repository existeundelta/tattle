import os
import json
import logging

from time import time
from queue import Queue
from threading import Thread
import multiprocessing

import requests, re
from bs4 import BeautifulSoup
from itertools import permutations
from string import ascii_lowercase, digits

# find buckets with files with these  
regex = re.compile("(\.zip|\.pem|\.sql|\.csv|\.xls|\.doc)", re.I)

POOLSIZE = multiprocessing.cpu_count() * 4

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
   
def check(url):
    logger.info('Checking %s', url)
    full = 'http://%s.s3.amazonaws.com/' % url
    response = requests.head(full)
    if response.status_code == 200:
        print "Found     :: %s" % full
        with open("cache.csv", 'a') as outfile:
            outfile.write(full+'\n')
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

class BucketFinder(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        
    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url = self.queue.get()
            try:
                check(url)            
            except:
                print "Failed   :: %s" % url
            self.queue.task_done()

def main():
    ts = time()
    
    # Create a queue to communicate with the worker threads
    queue = Queue()
    
    # Create worker threads
    for x in range(POOLSIZE):
        worker = BucketFinder(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
        
    # Put the tasks into the queue as a tuple    
    with open("words.txt") as infile: 
        urls = infile.read().split('\n')
    
    urls = [''.join(chars) for chars in permutations(characters, 4)]
    urls = urls[urls.index('f3id'):]
    
    for url in urls:
        logger.info('Queueing {}'.format(url))
        queue.put(url)
    
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    print('Took {}'.format(time() - ts))
