#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PROPOSED BY THE BRAIN OF Gennie https://github.com/gegebhart
# BUILT ON TWEEPY CODE POSTED BY GITLAURA: https://github.com/gitlaura/get_tweets/blob/master/get_tweets.py

#cd ~/.GITS/users-specific_topical_retweeter/
#python3 ~/.GITS/users-specific_topical_retweeter/get_tweets.py ~/.GITS/users-specific_topical_retweeter/representatives_twitter_accounts.txt

# 2do # Create crontab regular execution of script http://www.computerhope.com/unix/ucrontab.htm

# 2do # Automate the switch from initial run of 200 tweets to maintenance 20 tweet reruns

# 2do # Reduce tweet list file automatically

# 2do # search ALL keywords first, then decide whether or not to retweet... +1 for each found word then retweet if 0?

# 2do # inspect why certain rt's were retweeted, for example: https://twitter.com/cat803/status/791877532274470912
# (11/12 maybe fixed?)

# 2do # manipulate keywords var to be lowercase so to allow users to enter any case variation

#Update to follow lists rather than individuals (will require an updated retweet detector, but consume less API requests)
#http://stackoverflow.com/questions/39171301/tweepy-getting-the-author-of-a-retweeted-tweet
#http://stackoverflow.com/questions/27095950/tweepy-finding-the-original-author-of-a-retweet


#https://twitter.com/tweetcongress/lists/senate
#https://twitter.com/tweetcongress/lists/republican
#https://twitter.com/tweetcongress/lists/congress
#https://twitter.com/tweetcongress/lists/house-committee
#https://twitter.com/richarda/lists/top-50-us-politics
#https://twitter.com/verified/lists/us-congress
#https://twitter.com/gov/lists/us-house
#https://twitter.com/gov/lists/us-senate
#https://twitter.com/gov/lists/us-cabinet
#https://twitter.com/gov/lists/us-governors
#https://twitter.com/gov/lists/presidential-candidates
#https://twitter.com/gov/lists/us-secretaries-of-state
#https://twitter.com/gov/lists/us-senate

import sys
import os
import tweepy #http://www.tweepy.org/

# Retrieve Twitter API credentials
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"
with open(twitterKEYfile, 'r') as f:
    e = f.read()
    keys = e.split(',')
    consumer_key = keys[0]  #consumer_key
    consumer_secret = keys[1]  #consumer_secret
    access_key = keys[2]  #access_key
    access_secret = keys[3]  #access_secret
# http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Set count to however many tweets you want; Twitter only allows max 200 at once
number_of_tweets = 200 #initial run
#number_of_tweets = 20 #reruns

with open(os.path.expanduser('~') + '/.GITS/users-specific_topical_retweeter/keywords.txt', 'r') as keywordfile:
    keywords = keywordfile.read().splitlines()

# Method to get a user's last # tweets
def get_tweets(username):

    # Get tweets
    tweets = api.user_timeline(screen_name = username,count = number_of_tweets)
    ## API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
    ## API.update_with_media(filename[, status][, in_reply_to_status_id][, lat][, long][, source][, place_id][, file])
    #API.retweet(id)

	# For each tweet...
    for tweet in tweets:

		# Check to see if you have already scanned it
        with open("tweet_id_cachelist.txt", 'r') as cachefile:
            cachelist = cachefile.read()
            result = cachelist.find(tweet.id_str)
            #print(tweet.id_str)
            #print(cachefile.read())
            #print(cachelist)
            #print (result)

			# If not, add its ID to the cachefile
            if result == -1:
#                print ("Tweet ID " +tweet.id_str+ " is being added to cache")
                with open("tweet_id_cachelist.txt", 'a') as cachefile:
                    cachefile.write(tweet.id_str + "\n")
                    #print ("tweetid == id on line,return triggered")

                    # Process the tweet to lowercase
                    text = tweet.text.encode("utf-8").lower()

					# Make sure it's not a retweet
                    if not "rt @" in text:

						# Cycle through keywords
                        for word in keywords:
							# If the tweet contains a keyword...
                            if word in text:
								# Print notification
                                print ("Keyword(s) found tweet has been added to retweet_list.txt")
                                user = username.replace('\n', '').replace('\r', '')
                                # Preserve tweet link in text doc
                                tweetable = "https://twitter.com/"+user+"/status/"+tweet.id_str + "\n"
                                #print(tweet.text.encode("utf-8"))
                                #print(tweetable)
                                with open("retweet_list.txt", 'a') as retweetfile:
                                    retweetfile.write(tweetable)
                            	# Retweet from account owner of the used API keys
                                tweetthis = api.retweet(tweet.id_str)
                                print ("Tweeted: " + tweetable)

			# If you have already scanned the tweet, move on
            if result != -1:
#                print ("Tweet already in cache at: " + str(result))
                pass

# When executing script, the final argument provided must be a list of twitter accounts.
# EXAMPLE "name_list.txt" in: python3 ~/.GITS/users-specific_topical_retweeter/get_tweets.py ~/.GITS/users-specific_topical_retweeter/name_list.txt
with open(sys.argv[1], 'r') as userfile:
    userlist = userfile.read().splitlines()

	# For each user, run the get_tweets function from above
    for line in userlist:
        username = line
        try:
            get_tweets(username)
            print ("Updated: " + username)
        ##except:
        # #   print (tweepy.error.TweepError)
        #except subprocess.CalledProcessError as exc:
        ##    print ('error: code={}, out="{}"')
        ##    print ("https://twitter.com/" + username)
        except tweepy.TweepError as e:
            if str(e.reason) == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                print ("Twitter rate limit exceeded pausing for 1 hr")
                import time
                time.sleep(3601)
            if str(e.reason) == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
                print ("Twitter rate limit exceeded pausing for 1 hr")
                import time
                time.sleep(3601)
            if "Max retries exceeded" in str(e.reason):
                print ("Twitter rate limit exceeded pausing for 1 hr")
                import time
                time.sleep(3601)
            if e.api_code == 34:
                print ("error   The account does not exist: https://twitter.com/" + username)

            else:
                print ("Tweepy error code: " + str(e.api_code) + "  " + str(tweepy.error.TweepError))
                print (e.reason)
                print ("https://twitter.com/" + username)
                pass
