"""List of common settings used"""
from os import getenv
from decouple import config

AWS_API_KEY = getenv('AWS_API_KEY', config('AWS_API_KEY', default=''))
AWS_API_SECRET_KEY = getenv('AWS_API_SECRET_KEY', config('AWS_API_SECRET_KEY', default=''))
TWITTER_BEARER_TOKEN = getenv('TWITTER_BEARER_TOKEN', config('TWITTER_BEARER_TOKEN', default=''))
AWS_ACCESS_TOKEN = getenv('AWS_ACCESS_TOKEN', config('AWS_ACCESS_TOKEN', default=''))
AWS_ACCESS_TOKEN_SECRET = getenv('AWS_ACCESS_TOKEN_SECRET', config('AWS_ACCESS_TOKEN_SECRET', default=''))

AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID', config('AWS_ACCESS_KEY_ID', default=''))
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY', config('AWS_SECRET_ACCESS_KEY', default=''))

AWS_REGION_NAME = getenv('AWS_REGION_NAME', config('AWS_REGION_NAME', default='us-east-1'))
AWS_FIREHOSE_DELIVERY_STREAM = getenv('AWS_FIREHOSE_DELIVERY_STREAM',
                                      config('AWS_FIREHOSE_DELIVERY_STREAM', default=''))

DEBUG_MODE = int(getenv('DEBUG_MODE', config('DEBUG_MODE', default='0')))

# DATABASE
DB_DIALECT = getenv('DB_DIALECT', config('DB_DIALECT', default='postgresql'))
DB_DRIVER = getenv('DB_DRIVER', config('DB_DRIVER', default='psycopg2'))
DB_USERNAME = getenv('DB_USERNAME', config('DB_USERNAME', default='dex_user'))
DB_PASSWORD = getenv('DB_PASSWORD', config('DB_PASSWORD', default='db_pass'))
DB_HOST = getenv('DB_HOST', config('DB_HOST', default='localhost'))
DB_PORT = getenv('DB_PORT', config('DB_PORT', default='5432'))
DB_NAME = getenv('DB_NAME', config('DB_NAME', default='db_name'))