from modules import get, helpers
from flask import Blueprint, Flask, request, redirect, render_template, Response
import config
from modules.client.logs import print_with_seperator
from modules import yt
import threading
import time

# TODO: what is this.

client_videos = Blueprint("client_videos", __name__)
videos_dict = {}

def add_route(item):
    item_hash = hash(item)
    videos_dict[item_hash] = item
    return item_hash

def delete_route(item_hash):
    time.sleep(15)
    videos_dict.pop(item_hash)

@client_videos.route("/getURL", methods=['POST'])
@client_videos.route("/<int:res>/getURL", methods=['POST'])
def getURL(res=None):
    data = request.json
    if request.headers.get('HLS-Video'):
        url = yt.data_to_hls_url(data, res)
        item_hash = add_route(url)
        t = threading.Thread(target=delete_route, args=(item_hash,))
        t.start()
        return f'{request.root_url}/getURLFinal/{item_hash}'
    else:
        return yt.data_to_medium_url(data)
    
@client_videos.route("/getURLFinal/<item_hash>")
def getURLFinal(item_hash):
    item_hash = int(item_hash)
    return Response(videos_dict[item_hash], mimetype="application/vnd.apple.mpegurl")