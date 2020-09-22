import logging
import configparser

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener


logger = logging.getLogger()


def create_api():

    config = configparser.ConfigParser()
    config.read('config/config.ini')
    twitter_config = config['TWITTER']

    API_KEY = twitter_config['API_KEY']
    API_SECRET_KEY = twitter_config['API_SECRET_KEY']
    ACCESS_TOKEN = twitter_config['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = twitter_config['ACCESS_TOKEN_SECRET']

    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e

    logger.info("API created")
    
    return api