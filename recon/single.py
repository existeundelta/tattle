import json
import logging
import os
from pathlib import Path
from urllib.request import urlopen, Request
from time import time

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

def main():
   ts = time()
   client_id = os.getenv('IMGUR_CLIENT_ID')
   if not client_id:
       raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
   download_dir = setup_download_dir()
   links = [l for l in get_links(client_id) if l.endswith('.jpg')]
   for link in links:
       download_link(download_dir, link)
   print('Took {}s'.format(time() - ts))

if __name__ == '__main__':
   main()  
    