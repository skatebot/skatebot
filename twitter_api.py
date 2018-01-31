import twitter

import config


class Twitter(object):
    def __init__(self):
        self.twitter = twitter.Api(consumer_key=config.consumer_key,
                                   consumer_secret=config.consumer_secret,
                                   access_token_key=config.access_token_key,
                                   access_token_secret=config.access_token_secret, tweet_mode="extended")
        self.sent_posts = [tweet.id for tweet in self.get_tweets()]

    def get_tweets(self):
        return self.twitter.GetUserTimeline(user_id=config.twitter_id)

    def get_new_tweets(self):
        tweets = self.get_tweets()
        new_tweets = list(filter(lambda tweet: tweet.id not in self.sent_posts, tweets))
        self.sent_posts.extend([tweet.id for tweet in new_tweets])
        return new_tweets
