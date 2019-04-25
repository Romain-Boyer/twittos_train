import tweepy

import credentials_twitter as ct

auth = tweepy.OAuthHandler(ct.CONSUMER_KEY, ct.CONSUMER_SECRET)
auth.set_access_token(ct.ACCESS_TOKEN, ct.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        print('- ' * 30)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['python'])
