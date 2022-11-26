import itertools
import json
import logging
import re
import typing

from fastapi import FastAPI
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from sqlalchemy import desc
from starlette.responses import Response

from libs.models.tweets import Tweets

app = FastAPI()


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


@app.get('/tweets/popular/{limit}', response_class=PrettyJSONResponse)
def user_list(limit: int):
    tweets = Tweets.get_query_by_filter(columns=[Tweets.text, Tweets.retweets]).\
        order_by(desc(Tweets.retweets)).limit(limit).all()

    return {'tweets': tweets}


@app.get('/hashtags/popular/{limit}', response_class=PrettyJSONResponse)
def user_list(limit: int):
    tweets = Tweets.get_query_by_filter(columns=[Tweets.text]).all()
    logging.info(f'Tweets count: {len(tweets)}')
    hashtags = []
    for tweet in tweets:
        text = tweet[0]
        if "#" in text:
            for tag in text.split():
                if tag.startswith("#"):
                    hashtags.append(tag.strip("#").lower())
    tags_dict = {i: hashtags.count(i) for i in hashtags}
    d = dict(sorted(tags_dict.items(), key=lambda item: item[1], reverse=True))

    return {'hashtags': dict(itertools.islice(d.items(), limit))}


@app.get('/words/popular/{limit}', response_class=PrettyJSONResponse)
def user_list(limit: int):
    tweets = Tweets.get_query_by_filter(columns=[Tweets.text]).all()
    logging.info(f'Tweets count: {len(tweets)}')
    all_tweets = ""
    for tweet in tweets:
        all_tweets += tweet[0]
    all_tweets = re.sub("#", "", all_tweets)
    all_tweets = re.sub("@", "", all_tweets)
    all_tweets = re.sub(r'\shttps.+\s', "", all_tweets)
    tokens = word_tokenize(all_tweets)
    words = [word.lower() for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    fdist1 = FreqDist(words)

    return {'words': {w[0]: w[1] for w in fdist1.most_common(limit)}}
