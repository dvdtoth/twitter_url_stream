Twitter URL stream
==================

Simple python script to extract a stream of tweets by hashtag/keyword and record them in Neo4j

Dependencies
------------
- Python 2.5 - 2.7
- tweepy: https://github.com/tweepy/tweepy
- py2neo: https://github.com/nigelsmall/py2neo

Setup
-----
```
pip install py2neo tweepy
```

Copy config-example.ini to config.ini and set your twitter API keys and Neo4J locations

Usage
-----
./twitter_url_stream.py keyword
