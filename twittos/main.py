import tweepy

import credentials_twitter as ct

auth = tweepy.OAuthHandler(ct.CONSUMER_KEY, ct.CONSUMER_SECRET)
auth.set_access_token(ct.ACCESS_TOKEN, ct.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
    print('- '*45)