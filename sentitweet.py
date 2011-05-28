#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A simple example of using the musicmetric sentiment analysis call to analyse the content of a tweet.

call with the id of a tweet status as an argument and the script will output whether it's 
very negative, negative, neutral, postive, or very positive

so the call:

python sentitweet.py 64466256081854464

should return:
>SunFest was a blast! Great stage, great sound, now let's get drunk!
>sentiment is positive

'''
import sys
import logging
import urllib2
log = logging.getLogger(__name__)

from simplejson import loads
from apikey_private import *
sentiment_words = {1:"very negative", 2:"negative", 3:"neutral", 4:"positive", 5:"very positive"}

def main(argv):
    log.debug("argv: {0}".format(argv))
    twitter_id = argv[1]
    #grab some data from twitter
    data = loads(urllib2.urlopen("http://api.twitter.com/1/statuses/show/{0}.json".\
                 format(twitter_id)).read())
    tweet_content = data["text"]
    
    #push to sentiment analysis
    print tweet_content
    raw_senti = loads(urllib2.urlopen("http://apib2.semetric.com/sentiment?token="+\
                      API_KEY, data = tweet_content).read())
    print "sentiment is", sentiment_words[raw_senti['response']['score']],
    print "confidence is", raw_senti['response']['confidence']
    return 0
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s')
    sys.exit(main(sys.argv))
