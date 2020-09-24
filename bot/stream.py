import sys
import os
import time
import logging
from datetime import datetime

import tweepy

from setup import create_api
from helper import get_cadidates_twitter_user_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TweeterElectionListener(tweepy.StreamListener):

    def __init__(self, output_file):
        super(TweeterElectionListener, self).__init__()
        self.output_file = output_file
        self.count = 0
    
    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        logger.info(tweet.text)
        print(tweet._json, file=self.output_file)
        self.output_file.flush()
        os.fsync(self.output_file.fileno())
    
    def on_error(self, status_code):
        logger.error(f"Error on Stream Listener. Code: {status_code}")
        
        if status_code == 420:
            self.count = self.count + 1
            delay = self.count * 120
            logger.error(f"Waiting {delay} seconds")
            time.sleep(delay)
            return True

        logger.error("Exiting the application")
        return False


def main():

    users_id = get_cadidates_twitter_user_id()

    api = create_api()
    
    output = open("data/stream_output.txt", "a")

    listener = TweeterElectionListener(output_file=output)
    
    stream = tweepy.Stream(auth=api.auth, listener=listener)

    try:
        
        logger.info(f'Start Streaming - {datetime.now()}.')
        stream.filter(follow=users_id)

    except KeyboardInterrupt as e :
        logger.info("Stop Streaming.")
    finally:
        logger.info('Stream Finished.')
        stream.disconnect()
        output.close()

    return

if __name__ == "__main__":
    main()