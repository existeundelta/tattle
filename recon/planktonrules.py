# -*- coding:utf-8 -*-
import re
import sys 
import json
import pickle

from collections import defaultdict

planktonrules = 'ur2467618'
features = pickle.load(open('features.pic'))
featureset = set(features)

# The script takes two file names as arguments.
with open(sys.argv[1]) as f:
   all = json.load(f)
with open(sys.argv[2]) as f:
   plank = json.load(f)

# Print the header.
sys.stdout.write('planktonrules\t' + \ 
      '\t'.join([re.sub('\W', '_', f) for f in features]) + '\n')

# Each line corresponds to a review.
for doc in all + plank:
   auth = 1 if doc['authid'] == planktonrules else 0
   counter = defaultdict(int)
   for i in xrange(len(doc['body'])-4):
      key = doc['body'][i:(i+4)]
      if key in featureset: counter[key] += 1
   sys.stdout.write(str(auth) + '\t' + \ 
         '\t'.join([str(counter[a]) for a in features]) + '\n')

#### loaded
         
# I have the IMDB reviews as JSON documents.
with open(sys.argv[1]) as f:
   all = json.load(f)

counter = defaultdict(int)
for doc in all:
   for i in xrange(len(doc['body'])-4):
      counter[doc['body'][i:(i+4)]] += 1


# Pickle the 1000 most used 4-grams.
features = sorted(counter, key=counter.get, reverse=True)[:1000]
pickle.dump(features, open('features.pic', 'w'))         
