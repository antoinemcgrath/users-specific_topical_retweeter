##THIS SCRIPT IS GREAT AS IT WILL FETCH MORE THAN THE LAST 200 TL_tweets
##api.GETUserTimeline is the result of adapting the script from a tweepy base to a python-twitter package
## Source tweepy version is at https://gist.github.com/yanofsky/5436496


for tweet in TL_tweets:
    print(datetime.strptime(tweet.id_str.encode("utf-8"), "%a %b %d %H:%M:%S %Y")) + "," + tweet.user.screen_name.encode("utf-8") + "," +  tweet.text.encode("utf-8") )

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#initialize a list to hold all the tweepy Tweets
def get_all_of_one_user(username):
    alltweets = []
    screen_name=username
    new_tweets = api.GetUserTimeline(screen_name = screen_name,count=1)   #make initial request for most recent tweets (200 is the maximum allowed count)
    alltweets.extend(new_tweets)     #save most recent tweets
    oldest = alltweets[-1].id - 1      #save the id of the oldest tweet less one
    while len(new_tweets) > 0:        #keep grabbing tweets until there are no tweets left to grab
            print "getting tweets before %s" % (oldest)
            new_tweets = api.GetUserTimeline(screen_name = screen_name,count=200,max_id=oldest)         #all subsequent requests use the max_id param to prevent duplicates
            alltweets.extend(new_tweets)         #save most recent tweets
            oldest = alltweets[-1].id - 1         #update the id of the oldest tweet less one
            print "...%s tweets downloaded so far" % (len(alltweets))
    return alltweets
