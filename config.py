import os

import redis
from werkzeug.utils import import_string


class Config(object):
    # Parse redis environment variables.
    redis_endpoint_url = "redis-13586.c10.us-east-1-4.ec2.cloud.redislabs.com:13586"
    REDIS_HOST, REDIS_PORT = tuple(redis_endpoint_url.split(":"))
    REDIS_PASSWORD = "iaoSP4hzu93CUCTkzu0kCSy24G3g5mxB"
    SECRET_KEY = os.environ.get("SECRET_KEY", "Optional default value")
    SESSION_TYPE = "redis"
    redis_client = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
    )
    SESSION_REDIS = redis_client
    # TODO: Auth...


class ConfigDev(Config):
    # DEBUG = True
    pass


class ConfigProd(Config):
    pass


def get_config() -> Config:
    return ConfigDev
