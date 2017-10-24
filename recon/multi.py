import os
import json
import logging

from time import time
from Queue import Queue
from threading import Thread
import multiprocessing

import requests, re
from bs4 import BeautifulSoup
from itertools import permutations
from string import ascii_lowercase, digits

# find buckets with files with these  
regex = re.compile("(\.zip|\.pem|\.key|\.sql|\.csv|\.xls|\.doc)", re.I)

POOLSIZE = multiprocessing.cpu_count() * 4

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
   
def trawl(url):
    logger.info('Trawling %s', url)
    full = 'http://%s.s3.amazonaws.com/' % url
    response = requests.head(full)
    if response.status_code == 200:
        response = requests.get(full)
        soup = BeautifulSoup(response.content, "lxml")
        contents = soup.find_all('contents')
        for each in contents:
            if re.search(regex, each.key.text):
                with open('results.csv', 'a') as csv:
                    name = each.key.text
                    stamp = each.lastmodified.text
                    size = each.size.text
                    line = '%s,%s,%s,%s,%s' % (url,full,name,stamp,size)
                    print line
                    csv.write(line.encode('utf-8', 'ignore'))

class BucketFinder(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        
    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url = self.queue.get()
            try:
                trawl(url)            
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
        worker.daemon = True
        worker.start()
            
    # rockyou-like dictionary
    with open("words.txt") as infile: 
        urls = infile.read().split('\n')
    
    urls += [''.join(chars) for chars in permutations(characters, 3)] 
    urls += [''.join(chars) for chars in permutations(characters, 4)] 

    urls = list(set(urls)) # make unique
    
    # Put the tasks into the queue as a tuple    
    for url in urls:
        logger.info('Queueing {}'.format(url))
        queue.put(url)
        
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    print('Took {}'.format(time() - ts))
