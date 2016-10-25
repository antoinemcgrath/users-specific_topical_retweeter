# users-specific_topical_retweeter
This script will fetch tweets from a list of specific twitter accounts and check to see if the tweet contains keywords that are of interest before retweeting.

Running this script requires that you have a twitter account, Twitter API keys/access and a list of users to follow. For instructions on this view file Getting_Started.txt


Once the Getting_Started.txt insturctions are followed you will be able to execute the scrypt in terminal.
The arguments are:
python3 get_tweets.py list_of_twitter_accounts.txt

For example:
python3 ~/.GITS/username_tweet_fetch/get_tweets.py ~/.GITS/username_tweet_fetch/representatives_twitter_accounts.txt

Will cause your API associate twitter account to start retweeting.
A list of tweets scanned (and retweeted if positive for your keywords) will be appended to tweet_id_cachelist.txt this list will prevent the script from rescanning and retweeting those tweets the next time you run the script.

THANK YOU Sunglight Foundation and Sunlight labs for the seed list of congressmembers twitter accounts: http://politwoops.sunlightfoundation.com/
It was used to start the list representatives_twitter_accounts.txt additional campagin accounts and congressional candidate accounts have been added to the list.
