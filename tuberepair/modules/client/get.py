from requests_cache import CachedSession
from jinja2 import Environment, FileSystemLoader
from flask import request
from datetime import timedelta, datetime
import requests
import json

# custom functions
import config
from . import helpers
from modules.client.logs import print_with_seperator

# cache yt's (or invidious's) video request
# mostly infos and links
info_cache = CachedSession('cache/info', expire_after=timedelta(hours=config.CACHE_INFO), backend=config.backend)

# cache to not spam the invidious instance
session = info_cache

def unix(unix="0"):
    return datetime.fromtimestamp(int(unix)).isoformat() + '.000Z'

# Will be used in another update, but WHEN??? HUH???
def unix_now():
    return datetime.now().isoformat() + '.000Z'

# jinja2 path
env = Environment(loader=FileSystemLoader('templates'))

# simplify requests
def fetch(url):
    try:
        # Without sending User-Agent, the instance wouldn't send any data for {url}/api/v1/videos ... Why?
        # EXPLAINATION: prevent bots from scraping other bots.
        url = session.get(url, headers={'User-Agent': 'TubeRepair'}, proxies=helpers.proxies)
        data = url.json()
        return data
    except requests.ConnectionError:
        print_with_seperator('INVIDIOUS INSTANCE FAILED!', 'red')

# If error logging is enable, detour the function.
if config.GET_ERROR_LOGGING:
    orig_fetch = fetch
    def fetch(url):
        data = orig_fetch(url)
        #print_with_seperator(data)
        if not data:
            print_with_seperator(f'request "{url}" returned nothing from instance.')
        elif 'error' in data:
            print_with_seperator(f'Invidious returned an error processing "{url}"\n----Error begins below----\n{data}\n----End of error----')
        return data

# read template from jinja2
def template(file, render_data):
    t = env.get_template(file)
    output = t.render(render_data)
    return output

# YT app will turn up nothing if 404 was passed.
def error():
    return "", 404