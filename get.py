# -------------------------- #
#    DON'T EVEN COMPLAIN.    #
# -------------------------- #

from urllib.request import urlopen
from requests_cache import CachedSession
from jinja2 import Environment, FileSystemLoader
from modules.timeconvert import unix
import datetime
import requests
import json

# custom functions
import config
from modules.logs import text

# cache to not spam the invidious instance
session = CachedSession('cache/channel_info', expire_after=300)
session_homepage = CachedSession('cache/featured', expire_after=3600)

# jinja2 path
env = Environment(loader=FileSystemLoader('templates'))

# search results, for both videos and channels
def search_results(query, category):
    # remove space character
    search_keyword = query.replace(" ", "%20")

    
    # print logs if enabled
    # guilty lol
    if config.SPYING == True:
        text('Searched: ' + query)
    
    # search by videos
    if category == "video":
        url = session.get(f"https://{config.URL}/api/v1/search?q={search_keyword}&type=video")
        data = url.json()
        t = env.get_template('search_results.jinja2')

        output = t.render({
            'data': data[:config.SEARCHED_VIDEOS],
            'unix': unix,
            'url': config.HOST
        })

        return output

    # search by channels
    if category == "channel":
        url = requests.get(f"https://{config.URL}/api/v1/search?q={search_keyword}&type=channel")
        data = url.json()

        t = env.get_template('search_results_channel.jinja2')

        output = t.render({
            'data': data,
            'url': config.HOST
        })

        return output

# featured videos
def featured_videos(popular, regioncode):
    # trending videos categories
    # there is better way to do this, but for now Freaky...
    apiurl = "https://" + config.URL + "/api/v1/trending?region=" + regioncode
    if popular == "most_popular_Film":
        apiurl = f"https://{config.URL}/api/v1/trending?type=Movies&region={regioncode}"
    if popular == "most_popular_Games":
        apiurl = f"https://{config.URL}/api/v1/trending?type=Gaming&region={regioncode}"
    if popular == "most_popular_Music":
        apiurl = f"https://{config.URL}/api/v1/trending?type=Music&region={regioncode}"

    # print logs if enabled
    if config.SPYING == True:
        text("Region code: " + regioncode)

    # fetch api from invidious
    url = session_homepage.get(apiurl)
    data = url.json()
    
    # get template
    t = env.get_template('featured.jinja2')

    output = t.render({
        'data': data[:config.FEATURED_VIDEOS],
        'unix': unix,
        'url': config.HOST
    })

    return output

def comments(videoid):
    # fetch invidious comments api
    url = session_homepage.get(f"https://{config.URL}/api/v1/comments/{videoid}?sortby={config.SORT_COMMENTS}")
    data = url.json()

    # get template
    t = env.get_template('comments.jinja2')

    output = t.render({
        'data': data['comments'],
        'unix': unix,
        'url': config.HOST
    })

    return output


def channel_info(channel_id):
    # fetch from... you guessed it
    url = session.get(f"https://{config.URL}/api/v1/channels/{channel_id}")
    data = url.json()

    # wow being not lazy is ea-zy
    channel_url = data['authorId']
    channel_name = data['author']
    channel_pic_url = data['authorThumbnails'][0]['url']
    sub_count = data['subCount']

    # get template
    t = env.get_template('channel_info.jinja2')

    output = t.render({
        'author': channel_name,
        'author_id': channel_url,
        'channel_pic_url': channel_pic_url,
        'subcount': sub_count,
        'url': config.HOST
    })

    return output

def uploads(channel_id):
    url = requests.get(f"https://{config.URL}/api/v1/channels/{channel_id}/latest")
    data = url.json()

    # get template
    t = env.get_template('uploads.jinja2')

    output = t.render({
        'data': data['videos'],
        'unix': unix,
        'url': config.HOST
    })

    return output

def channel_playlists(channel_id):
    url = requests.get(f"https://{config.URL}/api/v1/channels/{channel_id}/latest")
    data = url.json()

    # get template
    t = env.get_template('channel_playlists.jinja2')

    output = t.render({
        'data': data
    })
    
    return output

def playlist_videos(playlist_id):
    url = requests.get(f"https://{config.URL}/api/v1/playlists/{playlist_id}")
    data = url.json()

    # get template
    t = env.get_template('playlist_videos.jinja2')

    output = t.render({
        'data': data,
        'unix': unix,
        'url': config.HOST
    })
    
    return output