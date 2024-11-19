from requests_cache import CachedSession
from jinja2 import Environment, FileSystemLoader
from datetime import timedelta, datetime
import requests
import json

# custom functions
import config
from modules import helpers
from .logs import print_with_seperator

# cache to not spam the invidious instance
session = CachedSession('cache/info', expire_after=timedelta(hours=1))

def unix(unix):
    return datetime.fromtimestamp(int(unix)).isoformat() + '.000Z'

def unix_now(): # Will be used in another update
    return datetime.now().isoformat() + '.000Z'

# jinja2 path
env = Environment(loader=FileSystemLoader('templates'))

# simplify requests
def fetch(url):
    try:
        # Without sending User-Agent, the instance wouldn't send any data for {url}/api/v1/videos ... Why?
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

def template(file, render_data):
    t = env.get_template(file)
    output = t.render(render_data)
    return output

def error():
    return "",404

# convert subscriber to text
def subscribers(string):
    processed_string = string.replace('subscribers', '')
    # TODO: IS this suppose to return a int or string? We need to be clear here.

    if 'M' in processed_string:
        return int(float(processed_string.replace('M', '')) * 100000.0)

    if 'K' in processed_string:
        return int(float(processed_string.replace('K', '')) * 1000.0)
    
    else:
        return processed_string