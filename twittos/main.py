import tweepy
from elasticsearch import Elasticsearch

import credentials_twitter as ct

# Tweepy
auth = tweepy.OAuthHandler(ct.CONSUMER_KEY, ct.CONSUMER_SECRET)
auth.set_access_token(ct.ACCESS_TOKEN, ct.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Elastic
es = Elasticsearch()


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # print(status.__dict__)
        doc = dict()
        doc['RT'] = False
        if hasattr(status, 'retweeted_status'):
            try:
                doc['text'] = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                doc['text'] = status.retweeted_status.text
            doc['RT'] = True
        else:
            try:
                doc['text'] = status.extended_tweet["full_text"]
                if doc['text'].startswith('RT'):
                    doc['RT'] = True
            except AttributeError:
                doc['text'] = status.text
                if doc['text'].startswith('RT'):
                    doc['RT'] = True
        doc['id_str'] = status.id_str
        doc['created_at'] = status.created_at
        doc['lang'] = status.lang

        if status.lang not in ['en', 'fr']:
            return

        print(doc)
        # Index the tweet
        es.index(index="test-twittos", doc_type='tweet', body=doc)
        print('- ' * 30)


if __name__ == '__main__':
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(track=['#got'])
