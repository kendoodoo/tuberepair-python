from flask import Blueprint, request, redirect, send_file, render_template, Response
import config
from modules.client import get, helpers
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
                'url': url,
                'channel_id': channel_id
            })
        raise Exception("No Data was returned!")
    except:
        return get.error()


# get playlist's video
# TODO: fix the damn thing
@playlist.route("/feeds/api/playlists/<playlist_id>")
@playlist.route("/<int:res>/feeds/api/playlists/<playlist_id>")
def playlists_video(playlist_id, res=''):
    
    max_results = request.args.get('max-results')
    # TODO: Find out what it wants when this happens.
    # This happens on YouTube 2.0.0, when you load a video from the playlist it add this
    # for the playlist queue
    if max_results and max_results == '0':
        return get.error()
    if playlist_id.strip().lower() == '(null)':
        return get.error()
    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)

    currentPage, next_page = helpers.process_start_index(request)

    query = f'page={currentPage}'

    # Santize and stitch 
    query = query.replace('&', '&amp;')
    
    url = request.url_root + str(res)
    data = get.fetch(f"{config.URL}/api/v1/playlists/{playlist_id}?{query}")
    
    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if not data:
        next_page = None

    if data:
        return get.template('playlist_videos.jinja2',{
            'data': data['videos'],
            'unix': get.unix,
            'url': url,
            'next_page': next_page
        })
    
    return get.error()

# Playlist search (v2.0.0)
@playlist.route("/feeds/api/playlists/snippets")
@playlist.route("/<int:res>/feeds/api/playlists/snippets")
def playlists_search(res=''):
    
    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)

    search_keyword = request.args.get('q')

    if not search_keyword:
        return get.error()
    
    currentPage, next_page = helpers.process_start_index(request)
    
    # remove space character
    search_keyword = search_keyword.replace(" ", "%20")

    query = f'q={search_keyword}&type=playlist&page={currentPage}'

    # Santize and stitch 
    query = query.replace('&', '&amp;')
    
    url = request.url_root + str(res)
    data = get.fetch(f"{config.URL}/api/v1/search?{query}")
    
    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if not data:
        next_page = None,

    return get.template('channel_playlists.jinja2',{
            'data': data,
            'url': url,
            'next_page': next_page
        })