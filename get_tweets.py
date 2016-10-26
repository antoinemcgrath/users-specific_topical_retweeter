#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PROPOSED BY THE BRAIN OF Gennie https://github.com/gegebhart
# BUILT ON TWEEPY CODE POSTED BY GITLAURA: https://github.com/gitlaura/get_tweets/blob/master/get_tweets.py

#cd /Users/macbook/.GITS/users-specific_topical_retweeter/
#python3 ~/.GITS/users-specific_topical_retweeter/get_tweets.py ~/.GITS/users-specific_topical_retweeter/name_list.txt
#python3 ~/.GITS/users-specific_topical_retweeter/get_tweets.py ~/.GITS/users-specific_topical_retweeter/representatives_twitter_accounts.txt

import sys
import os
import tweepy #http://www.tweepy.org/

#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" # crsreports.com
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter02.csv" # climatecongress.info


# Retrieve Twitter API credentials
with open(twitterKEYfile, 'r') as f:
    e = f.read()
    keys = e.split(',')
    #print(keys)
    consumer_key = keys[0]  #consumer_key
    consumer_secret = keys[1]  #consumer_secret
    access_key = keys[2]  #access_key
    access_secret = keys[3]  #access_secret
#http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


#method to get a user's last 100 ?200 tweets
def get_tweets(username):

    #set count to however many tweets you want; twitter only allows 200 at once
    number_of_tweets = 200

    #get tweets
    tweets = api.user_timeline(screen_name = username,count = number_of_tweets)
    ## API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
    #tweets = api.user_timeline(screen_name = username,count = number_of_tweets)

    ## API.update_with_media(filename[, status][, in_reply_to_status_id][, lat][, long][, source][, place_id][, file])
    #API.retweet(id)

    for tweet in tweets:
        with open("tweet_id_cachelist.txt", 'r') as cachefile:
            cachelist = cachefile.read()
            result = cachelist.find(tweet.id_str)
            #print(tweet.id_str)
            #print(cachefile.read())
            #print(cachelist)
            #print (result)
            if result == -1:
#                print ("Tweet ID " +tweet.id_str+ " is being added to cache")
                with open("tweet_id_cachelist.txt", 'a') as cachefile:
                    cachefile.write(tweet.id_str + "\n")
                    #print ("tweetid == id on line,return triggered")
                    if ("climate change" or "Climate change" or "Climate Change" or "Global Warming" or "global warming" or "globalwarming" or "climate" or "climatechange" or "GlobalWarming" or "Climate" or "climatechange") in str(tweet.text.encode("utf-8")):
#                    if ("CRS" or "crs") in str(tweet.text.encode("utf-8")):
                        if not ("RT @") in str(tweet.text.encode("utf-8")):

                            print ("Keyword(s) found tweet has been added to retweet_list.txt")
                            user = username.replace('\n', '').replace('\r', '')

                            #Preserve tweet link in word doc
                            tweetable = "https://twitter.com/"+user+"/status/"+tweet.id_str + "\n"
                            #print(tweet.text.encode("utf-8"))
                            #print(tweetable)
                            with open("retweet_list.txt", 'a') as retweetfile:
                                retweetfile.write(tweetable)

                            #reTweet from account owner of the used API keys
                            tweetthis = api.retweet(tweet.id_str)
                            print ("Tweeted: " + tweetable)


            if result != -1:
#                print ("Tweet already in cache at: " + str(result))
                pass

# When executing script the final argument provided must be a list of twitter accounts
# EXAMPLE "name_list.txt" in: python3 ~/.GITS/users-specific_topical_retweeter/get_tweets.py ~/.GITS/users-specific_topical_retweeter/name_list.txt
with open(sys.argv[1], 'r') as userfile:
    userlist = userfile.read().splitlines()

    for line in userlist:
        username = line
        try:
            get_tweets(username)
            print ("Updated: " + username)
        except:
            print (tweepy.error.TweepError)
        #except subprocess.CalledProcessError as exc:
            print ('error: code={}, out="{}"')
