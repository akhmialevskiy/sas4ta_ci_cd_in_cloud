"""Modul with list of constants used"""

# List of filter parameters.
# From https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream

# This fields parameter enables you to select which specific Tweet fields will deliver in each returned Tweet object
FILTER_TWEET_FIELDS_LIST = [
    'attachments',
    'author_id',
    'context_annotations',
    'conversation_id',
    'created_at',
    'edit_controls',
    'entities',
    'geo',
    'id',
    'in_reply_to_user_id',
    'lang',
    'public_metrics',
    'possibly_sensitive',
    'referenced_tweets',
    'reply_settings',
    'source',
    'text',
    'withheld'
]
# Expansions enable you to request additional data objects that relate to the originally returned Tweets
FILTER_EXPANSIONS_LIST = [
    'attachments.poll_ids',
    'attachments.media_keys',
    'author_id',
    'edit_history_tweet_ids',
    'entities.mentions.username',
    'geo.place_id',
    'in_reply_to_user_id',
    'referenced_tweets.id',
    'referenced_tweets.id.author_id'
]
# This fields parameter enables you to select which specific media fields will deliver in each returned Tweet.
FILTER_MEDIA_FIELDS_LIST = [
    'duration_ms',
    'height',
    'media_key',
    'preview_image_url',
    'type',
    'url',
    'width',
    'public_metrics',
    'alt_text',
    'variants'
]
# This fields parameter enables you to select which specific place fields will deliver in each returned Tweet.
FILTER_PLACE_FIELDS_LIST = [
    'contained_within',
    'country',
    'country_code',
    'full_name',
    'geo',
    'id',
    'name',
    'place_type'
]
# This fields parameter enables you to select which specific poll fields will deliver in each returned Tweet.
FILTER_POLL_FIELDS_LIST = [
    'duration_minutes',
    'end_datetime',
    'id',
    'options',
    'voting_status'
]
# This fields parameter enables you to select which specific user fields will deliver in each returned Tweet.
FILTER_USER_FIELDS_LIST = [
    'created_at',
    'description',
    'entities',
    'id',
    'location',
    'name',
    'pinned_tweet_id',
    'profile_image_url',
    'protected',
    'public_metrics',
    'url',
    'username',
    'verified',
    'withheld'
]
