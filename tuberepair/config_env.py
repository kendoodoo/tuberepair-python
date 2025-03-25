import os
from requests_cache import RedisCache
from modules.client import helpers

OSEnv = os.environ

def string_to_bool(input):
    if not isinstance(input, str):
        raise ValueError("A String was not passed")
    lower_input = input.lower()
    if lower_input == "true":
        return True
    elif lower_input == "false":
        return False
    raise ValueError("This string isn't true of false!")

if "USE_REDIS" in OSEnv:
    USE_REDIS = string_to_bool(OSEnv["USE_REDIS"])
    backend = RedisCache(host=OSEnv["REDIS_HOST"], port=OSEnv["REDIS_PORT"])

if "USE_INNERTUBE" in OSEnv:
    USE_INNERTUBE = string_to_bool(OSEnv["USE_INNERTUBE"])

if "CLIENT_TEST" in OSEnv:
    CLIENT_TEST = string_to_bool(OSEnv["CLIENT_TEST"])

if "MEDIUM_QUALITY" in OSEnv:
    MEDIUM_QUALITY = string_to_bool(OSEnv["MEDIUM_QUALITY"])

if "GET_ERROR_LOGGING" in OSEnv:
    GET_ERROR_LOGGING = string_to_bool(OSEnv["GET_ERROR_LOGGING"])

if "HLS_RESOLUTION" in OSEnv:
    HLS_RESOLUTION = int(OSEnv["HLS_RESOLUTION"])

if "URL" in OSEnv:
    URL = OSEnv["URL"]

if "PROXY" in OSEnv:
    helpers.setup_proxies(OSEnv["PROXY"])

if "RESMAX" in OSEnv and OSEnv["RESMAX"].isdigit():
    RESMAX = int(OSEnv["RESMAX"])

if "PORT" in OSEnv:
    PORT = OSEnv["PORT"]

if "DEBUG" in OSEnv:
    DEBUG = string_to_bool(OSEnv["DEBUG"])

if "SPYING" in OSEnv:
    SPYING = string_to_bool(OSEnv["SPYING"])

if "COMPRESS" in OSEnv:
    COMPRESS = string_to_bool(OSEnv["COMPRESS"])

if "FEATURED_VIDEOS" in OSEnv:
    FEATURED_VIDEOS = min(int(OSEnv["FEATURED_VIDEOS"]), 50)

if "COMMENTS" in OSEnv:
    COMMENTS = min(int(OSEnv["COMMENTS"]), 20)

if "SORT_COMMENTS" in OSEnv:
    SORT_COMMENTS = OSEnv["SORT_COMMENTS"]
