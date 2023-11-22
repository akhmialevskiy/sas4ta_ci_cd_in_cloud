import json
import boto3
import codecs
import logging

from libs.models.users import Users
from libs.models.tweets import Tweets

S3_BUCKET_NAME = 's3-tta-bucket'
s3 = boto3.client('s3')
# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    file_name = event['Records'][0]['s3']['object']['key']
    print(f'File Name: {file_name}')

    s3_object = s3.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
    line_stream = codecs.getreader("utf-8")

    for line in line_stream(s3_object['Body']):
        tweet = json.loads(line)

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
