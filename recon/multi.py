import os
import json
import logging

from pathlib import Path
from urllib.request import urlopen, Request
from time import time
from queue import Queue
from threading import Thread
import multiprocessing

POOLSIZE = multiprocessing.cpu_count()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def get_links(client_id):
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    request = Request('https://api.imgur.com/3/gallery/', headers=headers, method='GET')
    with urlopen(request) as response:
        data = json.loads(response.readall().decode('utf-8'))
    return map(lambda item: item['link'], data['data'])

def download_link(directory, link):
    logger.info('Downloading %s', link)
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.readall())

def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            download_link(directory, link)
            self.queue.task_done()

def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create worker threads
    for x in range(POOLSIZE):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
        
    # Put the tasks into the queue as a tuple
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
        
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    print('Took {}'.format(time() - ts))
    