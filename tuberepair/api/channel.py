from modules import get
from flask import Blueprint, Flask, request, redirect, render_template
import config
from modules.logs import text

channel = Blueprint("channel", __name__)

# get channel info
@channel.route("/feeds/api/channels/<channel_id>")
@channel.route("/<res>/feeds/api/channels/<channel_id>")
def search(channel_id, res=''):
    url = request.url_root + res 
    # fetch from... you guessed it
    data = get.fetch(f"{config.URL}/api/v1/channels/{channel_id}")

    if data:
        # wow being not lazy is ea-zy
        channel_url = data['authorId']
        channel_name = data['author']
        channel_pic_url = data['authorThumbnails'][0]['url']
        sub_count = data['subCount']

        return get.template('channel_info.jinja2',{
            'author': channel_name,
            'author_id': channel_url,
            'channel_pic_url': channel_pic_url,
            'subcount': sub_count,
            'url': url
        })
    
    return get.error()

# search for channels
@channel.route("/feeds/api/channels")
@channel.route("/<res>/feeds/api/channels")
def channels(res=''):
    url = request.url_root + res 
    query = request.args.get('q')
    data = get.fetch(f"{config.URL}/api/v1/search?q={query}&type=channel")

    if data:

        # template
        return get.template('search_results_channel.jinja2',{
            'data': data,
            'url': url
        })

    return get.error()
    

@channel.route("/feeds/api/users/<channel_id>/uploads")
@channel.route("/<res>/feeds/api/users/<channel_id>/uploads")
def uploads(channel_id, res=''):
    url = request.url_root + res 
    data = get.fetch(f"{config.URL}/api/v1/channels/{channel_id}/latest")

    if data:
        return get.template('uploads.jinja2',{
            'data': data['videos'],
            'unix': get.unix,
            'url': url
        })
    
    return get.error()
