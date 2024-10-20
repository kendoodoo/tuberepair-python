from flask import Blueprint, request, redirect, send_file, render_template, Response
import config
from modules import get
from jinja2 import Environment, FileSystemLoader

playlist = Blueprint("playlist", __name__)

# jinja2 path
env = Environment(loader=FileSystemLoader('templates'))

# get playlists
# TODO: get more video info since invidious simplified it.
@playlist.route("/feeds/api/users/<channel_id>/playlists")
@playlist.route("/<int:res>/feeds/api/users/<channel_id>/playlists")
def playlists(channel_id, res=''):

    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)
    
    url = request.url_root + str(res) 
    continuationToken = request.args.get('continuation') and '?continuation=' + request.args.get('continuation') or ''
    try:
        data = get.fetch(f"{config.URL}/api/v1/channels/{channel_id}/playlists{continuationToken}")

        # Templates have the / at the end, so let's remove it.
        if url[-1] == '/':
            url = url[:-1]
        
        if data:
            return get.template('channel_playlists.jinja2',{
                'data': data['playlists'],
                'continuation': 'continuation' in data and data['continuation'] or None,
                'url': url
            })
        raise Exception("No Data was returned!")
    except:
        return get.error()


# get playlist's video
# TODO: fix the damn thing
@playlist.route("/feeds/api/playlists/<playlist_id>")
@playlist.route("/<int:res>/feeds/api/playlists/<playlist_id>")
def playlists_video(playlist_id, res=''):
    
    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)
    
    url = request.url_root + str(res) 
    data = get.fetch(f"{config.URL}/api/v1/playlists/{playlist_id}")
    
    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if data:
        return get.template('playlist_videos.jinja2',{
            'data': data['videos'],
            'unix': get.unix,
            'url': url
        })
    
    return get.error()