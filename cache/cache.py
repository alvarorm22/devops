# app.py
import os
import json
import sys
from datetime import timedelta

import httpx
import redis
import flask

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=6379,
            password=os.getenv('REDIS_PASSWORD'),
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            print ("Connected to Redis")
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


client = redis_connect()


def get_json_from_api() -> dict:
    """Data from api."""

    with httpx.Client() as client:
        url = "http://api2json:5000/api/v1/resources/airq"

        response = client.get(url)
        return response.json()


def get_json_from_cache(key: str) -> str:
    """Data from redis."""

    val = client.get(key)
    return val


def set_json_to_cache(key: str, value: str) -> bool:
    """Data to redis."""

    state = client.setex(key, timedelta(seconds=3600), value=value,)
    return state


def get_measures_json(keyredis: str) -> dict:

    # First it looks for the data in redis cache
    data = get_json_from_cache(key=keyredis)
    # If cache is found then serves the data from cache
    if data is not None:
        data = json.loads(data)
        data["cache"] = True
        return data

    else:
        # If cache is not found then sends request to the API
        data = get_json_from_api()

        # This block sets saves the respose to redis and serves it directly
        data["cache"] = False
        data = json.dumps(data)
        state = set_json_to_cache(key=keyredis, value=data)

        if state is True:
            return json.loads(data)
        return data


app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    return "<h1>REDIS CACHE API</h1>"



@app.route('/api/v1/measures/air')
def view() -> dict:
    keyredis="measures"
    return get_measures_json(keyredis)

app.run(host='0.0.0.0', port=5005)
