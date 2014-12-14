#!/usr/bin/python

""" Follow URL stream by keyword on twitter
Author: David Toth http://github.com/dvdtoth
"""

import sys
import argparse
import json
import tweepy
import webbrowser
import re
import urllib2
from ConfigParser import SafeConfigParser
from py2neo import Graph, Node, Relationship, watch

# Parse config file 
Config = SafeConfigParser()
Config.read("config.ini")
consumer_key = Config.get('twitter_keys', 'consumer_key')
consumer_secret = Config.get('twitter_keys', 'consumer_secret')
access_token = Config.get('twitter_keys', 'access_token')
access_token_secret = Config.get('twitter_keys', 'access_token_secret')

graph = Graph(Config.get('neo4j', 'uri'))

# Parse arguments
argparser = argparse.ArgumentParser(description='Extract URLs from a twitter stream')
argparser.add_argument('keyword', help='Keyword to look for')
args = argparser.parse_args()

urlset = set()

print 'Start streaming of "' + args.keyword + '" related tweets'

def extracturl(url):
        """ Follow redirects and extract urls """
        try:
                f = urllib2.urlopen(url)
                # Open unique urls
                if f not in urlset:
                        urlset.add(f.url)
                        print f.url
                        # webbrowser.register("osx", webbrowser.MacOSX)
                        # b = webbrowser.get("osx")
                        # b.open_new_tab(u)
        except:
                print 'Couldn\'t open: ' + url

def pushTweetToGraph(tweet):
	user = Node("User", name=tweet['user']['screen_name'])
	tweet = keyword
	graph.create(user)
	graph.create(tweet, (user, "TWEETED", 0))


class StdOutListener(tweepy.streaming.StreamListener):
        """ Start Tweepy listener """
        def on_data(self, data):
                tweet = json.loads(data)
		pushTweetToGraph(tweet)
		print json.dumps(tweet,sort_keys=True,indent=4)
                # Find urls
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet['text'])
                for u in urls:
                        extracturl(u)

        def on_error(self, status):
                print status


if __name__ == '__main__':
	keyword = Node("Keyword", name=args.keyword)
	graph.create(keyword)
        l = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = tweepy.Stream(auth, l)
        stream.filter(track=[args.keyword])
