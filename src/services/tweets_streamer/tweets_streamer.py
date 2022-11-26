"""Main module for tweets streaming"""
import json
import logging
import signal
import sys

import boto3
import tweepy
from botocore.exceptions import ClientError

from libs.constants import (
    FILTER_EXPANSIONS_LIST,
    FILTER_MEDIA_FIELDS_LIST,
    FILTER_PLACE_FIELDS_LIST,
    FILTER_POLL_FIELDS_LIST,
    FILTER_TWEET_FIELDS_LIST,
    FILTER_USER_FIELDS_LIST
)
from libs.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_BEARER_TOKEN,
    AWS_FIREHOSE_DELIVERY_STREAM,
    AWS_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    DEBUG_MODE
)

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def signal_handler(sig_num, stack_frame):
    """Signal handler function.

    :param sig_num: Signal number
    :type sig_num: int
    :param stack_frame: Stack frame
    :type stack_frame:
    """
    logger.warning(f'Signal {sig_num} received. Exit')
    if DEBUG_MODE:
        logger.warning(stack_frame)
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

    def put_tweet_record(self, tweet_data: bytes) -> None:
        """Put tweets to the AWS Firehose stream.

        :param tweet_data: Tweet data get from Tweet API
        :type tweet_data: bytes
        """
        try:
            self.client.put_record(
                DeliveryStreamName=self.delivery_stream,
                Record={'Data': f'{tweet_data.decode("utf-8")}\n'}
            )
        except ClientError as error:
            logger.error(f'Failed to put data to the Firehose stream: {error}')

    def on_connect(self):
        """This function gets called when the stream is working
        """
        logger.info("Connected to the Twitter Developer API.")

    def on_data(self, raw_data: bytes):
        """This is called when raw data is received from the stream.
        This method handles sending the data to other methods.

        :param raw_data: The raw data from the stream
        :type raw_data: bytes
        """

        # Stop stream on SIGINT signal
        signal.signal(signal.SIGINT, signal_handler)

        # Put tweet to stream
        self.put_tweet_record(tweet_data=raw_data)

        tweet = json.loads(raw_data)
        if "errors" in tweet:
            self.on_errors(tweet["errors"])

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
