from modules import get, helpers
from flask import Blueprint, Flask, request, redirect, render_template
import config
from modules.logs import print_with_seperator

channel = Blueprint("channel", __name__)

# get channel info
@channel.route("/feeds/api/channels/<channel_id>")
@channel.route("/<int:res>/feeds/api/channels/<channel_id>")
def search(channel_id, res=''):
    
    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)
    
    url = request.url_root + str(res) 
    # fetch from... you guessed it
    data = get.fetch(f"{config.URL}/api/v1/channels/{channel_id}")

    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    # Error handling
    if data and 'error' in data:
        return get.error()
    
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

# search for channels
@channel.route("/feeds/api/channels")
@channel.route("/<int:res>/feeds/api/channels")
def channels(res=''):
    
    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)
    
    url = request.url_root + str(res) 
    query = request.args.get('q')
    current_page, next_page = helpers.process_start_index(request)
    data = get.fetch(f"{config.URL}/api/v1/search?q={query}&type=channel&page={current_page}")

    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if not data:
        next_page = None

        # template
    return get.template('search_results_channel.jinja2',{
        'data': data,
        'url': url,
        'next_page': next_page
    })

    #return get.error()
    

@channel.route("/feeds/api/users/<channel_id>/uploads")
@channel.route("/<int:res>/feeds/api/users/<channel_id>/uploads")
def uploads(channel_id, res=''):
    
    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)
    
    url = request.url_root + str(res) 
    continuation_token = request.args.get('continuation') and '&amp;continuation=' + request.args.get('continuation') or ''
    # https://docs.invidious.io/api/channels_endpoint/#get-apiv1channelsidvideos
    # Despite documention says /latest takes in a continuation token, it doesn't
    # sort_by is broken according to documention and will default to newest
    # we will add it anyway incase it ever gets fixed
    data = get.fetch(f"{config.URL}/api/v1/channels/{channel_id}/videos?sort_by=newest{continuation_token}")
    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if data:
        return get.template('uploads.jinja2',{
            'data': data['videos'],
            'unix': get.unix,
            'continuation': 'continuation' in data and data['continuation'] or None,
            'url': url
        })
    
    return get.error()
