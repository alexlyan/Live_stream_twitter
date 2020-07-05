# importing packages
import settings
# tweepy libraries
import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

# Libraries working with data
from textblob import TextBlob
from datetime import datetime
import re

# Access to database
from df_setup import engine

# credentials
from credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

# Class and functions
class StreamListener(tweepy.StreamListener):
    """Class for listening and inserting data into database"""
    #     def __init__(engine):
    #         engine = create_engine('sqlite:///server_db.db', echo=True)
    #         conn = engine.connect()

    def on_status(self, status):
        # data collection from twit stream
        if status._json['retweeted']:
            # Avoid retweeted info, and only original tweets will be received
            return True
        created_at = datetime.strptime(status._json['created_at'], '%a %b %d %H:%M:%S +%f %Y').strftime(
            '%Y-%m-%d %H:%M:%S')
        added_at = datetime.utcnow()
        id_user = status._json['user']['id']
        screen_name = status._json['user']['name']
        location = deEmojify(status._json['user']['location'])
        full_text = deEmojify(clean_tweet(fulltxt(status._json)))
        hashtags = hashtagstxt(status._json)
        retweet_count = status._json['retweet_count']
        sentiment_text = TextBlob(status._json['text']).sentiment
        polarity = sentiment_text.polarity
        subjectitivity = sentiment_text.subjectivity

        # access to database
        vals = (created_at, added_at, id_user, screen_name, location, full_text, hashtags, retweet_count, polarity,
                subjectitivity)
        query = "INSERT INTO twitter_table (Created_at, Added_at, Id_user, Username," \
                " Location, Text, Hashtags, Retweet_count, Polarity, " \
                "Subjectivity) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        conn = engine.connect()
        conn.execute(query, vals)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False


# Return full_text, if it is empty return 'text'
def fulltxt(tweet):
    try:
        return tweet['extended_tweet']['full_text']
    except KeyError as e:
        return tweet['text']


# Return hashtags in list, if it is empty return None
def hashtagstxt(tweet):
    if tweet or tweet != '':
        try:
            return ','.join([twit['text'] for twit in tweet['extended_tweet']['entities']['hashtags']])
        except KeyError as e:
            return None
    else:
        return None


# for review
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None


# For Cleaning tweet
def clean_tweet(tweet):
    '''
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("((@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|([^0-9A-Za-z \t]\w+)\
    |(\w+:\/\/\S+)|(RT)|(RT\s:))", " ", tweet).split())


if __name__ == '__main__':

    # Getting access to Twitter API
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Access to database
    # conn = engine.connect()
    twit_listen = StreamListener()
    stream = tweepy.Stream(auth=auth, listener=twit_listen)

    # List of tags
    tag_list = settings.Hashtags

    # Listening twits
    stream.filter(track=tag_list)
