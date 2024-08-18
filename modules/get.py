from requests_cache import CachedSession
from jinja2 import Environment, FileSystemLoader
from datetime import timedelta
from modules.timeconvert import unix
import requests
import json

# custom functions
import config
from modules.logs import text

# cache to not spam the invidious instance
session = CachedSession('cache/info', expire_after=timedelta(hours=1))

# jinja2 path
env = Environment(loader=FileSystemLoader('templates'))

# simplify requests
def fetch(url):
    url = session.get(url)
    data = url.json()
    return data

# search results, for both videos and channels
def search_results(query, category, url):
    # remove space character
    search_keyword = query.replace(" ", "%20")
    
    # print logs if enabled
    if config.SPYING == True:
        text('Searched: ' + query)
    
    # search by videos
    if category == "video":
        data = fetch(f"{config.URL}/api/v1/search?q={search_keyword}&type=video")
        t = env.get_template('search_results.jinja2')

        output = t.render({
            'data': data[:config.SEARCHED_VIDEOS],
            'unix': unix,
            'url': url
        })

        return output

    # search by channels
    if category == "channel":
        data = fetch(f"{config.URL}/api/v1/search?q={search_keyword}&type=channel")

        t = env.get_template('search_results_channel.jinja2')

        output = t.render({
            'data': data,
            'url': url
        })

        return output

# featured videos
def featured_videos(popular, regioncode, url):
    # trending videos categories
    # there is better way to do this, but for now Freaky...
    apiurl = config.URL + "/api/v1/trending?region=" + regioncode
    if popular == "most_popular_Film":
        apiurl = f"{config.URL}/api/v1/trending?type=Movies&region={regioncode}"
    if popular == "most_popular_Games":
        apiurl = f"{config.URL}/api/v1/trending?type=Gaming&region={regioncode}"
    if popular == "most_popular_Music":
        apiurl = f"{config.URL}/api/v1/trending?type=Music&region={regioncode}"

    # print logs if enabled
    if config.SPYING == True:
        text("Region code: " + regioncode)

    # fetch api from invidious
    data = fetch(apiurl)
    
    # get template
    t = env.get_template('featured.jinja2')

    output = t.render({
        'data': data[:config.FEATURED_VIDEOS],
        'unix': unix,
        'url': url
    })

    return output

def comments(videoid, url):
    # fetch invidious comments api
    data = fetch(f"{config.URL}/api/v1/comments/{videoid}?sortby={config.SORT_COMMENTS}")

    # get template
    t = env.get_template('comments.jinja2')

    output = t.render({
        'data': data['comments'],
        'unix': unix,
        'url': url
    })

    return output


def channel_info(channel_id, url):
    # fetch from... you guessed it
    data = fetch(f"{config.URL}/api/v1/channels/{channel_id}")

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
        'url': url
    })

    return output

def uploads(channel_id, url):
    data = fetch(f"{config.URL}/api/v1/channels/{channel_id}/latest")

    # get template
    t = env.get_template('uploads.jinja2')

    output = t.render({
        'data': data['videos'],
        'unix': unix,
        'url': url
    })

    return output

def channel_playlists(channel_id, url):
    data = fetch(f"{config.URL}/api/v1/channels/{channel_id}/latest")

    # get template
    t = env.get_template('channel_playlists.jinja2')

    output = t.render({
        'data': data
    })
    
    return output

def playlist_videos(playlist_id, url):
    data = fetch(f"{config.URL}/api/v1/playlists/{playlist_id}")

    # get template
    t = env.get_template('playlist_videos.jinja2')

    output = t.render({
        'data': data,
        'unix': unix,
        'url': url
    })
    
    return output
