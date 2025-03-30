from flask import Blueprint, request, g
import config
from modules.client import get, helpers

playlist = Blueprint("playlist", __name__)

# get playlists
# TODO: get more video info since invidious simplified it.
def playlists(channel_id, res=''):

    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)
    
    url = request.url_root + str(res) 
    continuationToken = request.args.get('continuation') and '?continuation=' + request.args.get('continuation') or ''
    try:
        data = get.fetch(f"{config.URL}/api/v1/channels/{channel_id}/playlists{continuationToken}")
        
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

    if not data:
        next_page = None,

    return get.template('channel_playlists.jinja2',{
            'data': data,
            'url': url,
            'next_page': next_page
        })

# worse than hell, but works
def assign(path, func):
    bprint = playlist
    # saves a ton of unnecessary
    bprint.add_url_rule(path, view_func=func)
    # here's your res, kevin
    bprint.add_url_rule("/<int:res>" + path, view_func=func)

assign("/feeds/api/users/<channel_id>/playlists", playlists)
assign("/feeds/api/playlists/<playlist_id>", playlists_video)
assign("/feeds/api/playlists/snippets", playlists_search)
