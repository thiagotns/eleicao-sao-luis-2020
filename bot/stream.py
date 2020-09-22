import sys
import time
import logging

import tweepy
from setup import create_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TweeterElectionListener(tweepy.StreamListener):
    
    def __init__(self, output_file=sys.stdout):
        super(TweeterElectionListener, self).__init__()
        self.output_file = output_file
    
    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        print(tweet.text, file=self.output_file)
    
    def on_error(self, status_code):
        logger.error(status_code)

def main():

    api = create_api()
    listener = TweeterElectionListener()
    
    stream = tweepy.Stream(auth=api.auth, listener=listener)

    try:
        
        logger.info('Start Streaming.')
        stream.filter(track=['eleição'])

    except KeyboardInterrupt as e :
        logger.info("Stop Streaming.")
    finally:
        logger.info('Stream Finished.')
        stream.disconnect()

    return

if __name__ == "__main__":
    main()