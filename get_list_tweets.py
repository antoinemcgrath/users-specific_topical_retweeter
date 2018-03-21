#!/usr/bin/python
###! /Users/macbook/anaconda2/bin/python3
# To run this script you will need the python-twitter package #pip install python-twitter
#get_list_tweets.py

#cd ~/.GITS/users-specific_topical_retweeter/
#python2 ~/.GITS/users-specific_topical_retweeter/get_list_tweets.py ~/.GITS/users-specific_topical_retweeter/representatives_twitter_accounts.txt


import twitter
import sys
import os


TSlug_List = "members-of-congress"
Number_of_Tweets = 200           #Max number of tweets returned is 200
TList_Owner = 'cspan'
RTs = False                                 #True/False

twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"

# get twitter API access credentials
with open(twitterKEYfile, 'r') as f:
    e = f.read()
    keys = e.split(',')
    consumer_key = keys[0]  #consumer_key
    consumer_secret = keys[1]  #consumer_secret
    access_key = keys[2]  #access_key
    access_secret = keys[3]  #access_secret
api = twitter.Api(consumer_key, consumer_secret,access_key, access_secret)


# get keywords (words of interes)
with open(os.path.expanduser('~') + '/.GITS/users-specific_topical_retweeter/keywords.txt', 'r') as keywordfile:
    keywords = keywordfile.read().splitlines()


# get list of previous cached tweets
with open(os.path.expanduser('~') + "/.GITS/users-specific_topical_retweeter/tweet_id_cachelist.txt", 'r') as cachefile:
    cachelist = cachefile.read()


# get tweets of a list
TL_tweets = api.GetListTimeline(list_id=None, slug=TSlug_List, owner_id=None, owner_screen_name=TList_Owner, since_id=None, max_id=None, count=Number_of_Tweets, include_rts=RTs, include_entities=True)


#
for tweet in TL_tweets:
    result = cachelist.find(tweet.id_str)
    if result == -1:
        #print ("Tweet ID " +tweet.id_str+ " is being added to cache")
        with open("tweet_id_cachelist.txt", 'a') as cachefile:
            ##cachefile.write(tweet.id_str + "\n")
            #print ("tweetid == id on line,return triggered")
            # Process the tweet to lowercase
            text = (tweet.text).encode("utf-8").lower()

            # Make sure it's not a retweet
            if not "rt @" in text:

                # Cycle through keywords
                for word in keywords:
                    # If the tweet contains a keyword...
                    if word in text:
                        # Print notification
                        print ("Keyword(s) found tweet has been added to retweet_list.txt")
                        ##user = username.replace('\n', '').replace('\r', '')
                        # Preserve tweet link in text doc
                        ##tweetable = "https://twitter.com/"+user+"/status/"+tweet.id_str + "\n"
                        #print(tweet.text.encode("utf-8"))
                        #print(tweetable)
                        ##with open("retweet_list.txt", 'a') as retweetfile:
                        ##    retweetfile.write(tweetable)
                        # Retweet from account owner of the used API keys
                        #tweetthis = api.retweet(tweet.id_str)
                        print ("Tweeted: " + (tweet.text).encode("utf-8"))
                        print ("Tweeted: " + (tweet.id_str).encode("utf-8"))


    # If you have already scanned the tweet, move on
    if result != -1:
#            print ("Tweet already in cache at: " + str(result))
        pass
