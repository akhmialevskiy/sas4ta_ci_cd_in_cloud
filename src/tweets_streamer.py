"""Main module for stream tweets"""
import json
import logging
import signal
import sys

import boto3
import tweepy
from botocore.exceptions import ClientError

from src.libs.constants import (
    FILTER_EXPANSIONS_LIST,
    FILTER_MEDIA_FIELDS_LIST,
    FILTER_PLACE_FIELDS_LIST,
    FILTER_POLL_FIELDS_LIST,
    FILTER_TWEET_FIELDS_LIST,
    FILTER_USER_FIELDS_LIST
)
from src.libs.models import Tweets, Users
from src.libs import (
    AWS_BEARER_TOKEN,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION_NAME,
    AWS_FIREHOSE_DELIVERY_STREAM, DEBUG_MODE
)


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def signal_handler(_signo, _stack_frame):
    logger.warning(f'Signal {_signo} received. Exit')
    sys.exit(0)


class TweetsStream(tweepy.StreamingClient):
    """Twitter streaming client"""

    def __init__(self, bearer_token: str):
        self.client = boto3.client('firehose',
                                   region_name=AWS_REGION_NAME,
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        self.delivery_stream = AWS_FIREHOSE_DELIVERY_STREAM
        super(TweetsStream, self).__init__(bearer_token=bearer_token)

    def put_tweet_record(self, tweet_data: str) -> None:
        """Put tweets to the AWS Firehose stream.

        :param tweet_data:
        :type tweet_data:
        """
        try:
            self.client.put_record(
                DeliveryStreamName=self.delivery_stream,
                Record={'Data': f'{tweet_data.decode("utf-8")}\n'}
            )
        except ClientError as error:
            logger.error(f'Failed to put data Firehose stream: {error}')

    def on_connect(self):
        """This function gets called when the stream is working
        """
        logger.info("Connected to Twitter API.")

    def on_data(self, data: str):
        """This is called when raw data is received from the stream.
        This method handles sending the data to other methods.

        :param data: The raw data from the stream
        :type data: str
        """

        # Stop stream on SIGINT signal
        signal.signal(signal.SIGINT, signal_handler)

        # Put tweet to stream
        self.put_tweet_record(tweet_data=data)

        tweet = json.loads(data)
        if "errors" in tweet:
            self.on_errors(tweet["errors"])

        if DEBUG_MODE:
            user_id = tweet['data']['author_id']
            author = Users(id=user_id)

            for user in tweet['includes']['users']:
                if user_id == user['id']:
                    author = Users(
                        id=user_id,
                        created=user['created_at'],
                        description=user['description'],
                        location=user.get('location', None),
                        followers=user['public_metrics']['followers_count'],
                        friends=user['public_metrics']['following_count'],
                        statuses=user['verified']
                    )
                    break

            tweet_text = tweet['data']['text']
            logger.info(f'Tweet text is: {tweet_text}')

            tweet_model = Tweets(
                id=tweet['data']['id'],
                text=tweet_text,
                create_time=tweet['data']['created_at'],
                retweets=tweet['data']['public_metrics']['retweet_count'],
                likes=tweet['data']['public_metrics']['like_count'],
                lang=tweet['data']['lang'],
                author=author
             )
            Tweets.add_tweet(tweet_model)

    def on_error(self, status):
        """This is called when errors are received.

        :param status: Error status
        :type status: dict
        """
        logger.error(f'Failed to handle tweet: {status}')


if __name__ == '__main__':
    stream = TweetsStream(bearer_token=AWS_BEARER_TOKEN)
    if DEBUG_MODE:
        stream.add_rules(add=tweepy.StreamRule('"breaking news"'))  # adding the rules

    stream.filter(
        expansions=FILTER_EXPANSIONS_LIST,
        media_fields=FILTER_MEDIA_FIELDS_LIST,
        place_fields=FILTER_PLACE_FIELDS_LIST,
        poll_fields=FILTER_POLL_FIELDS_LIST,
        tweet_fields=FILTER_TWEET_FIELDS_LIST,
        user_fields=FILTER_USER_FIELDS_LIST,
        threaded=False
    )
