# Version v0.0.2 (beta-1)
from flask import Flask, request, redirect, send_file, render_template, Response
from flask_compress import Compress
from uuid import uuid4
from waitress import serve
import hashlib
import random

# custom function
import config
from modules import logs, yt, get

# Load version
logs.version(config.VERSION)
app = Flask(__name__)

# use compression to load faster
if config.COMPRESS:
    compress = Compress(app)

# static contents (sort of)
# --------------------------------------------- #

@app.route("/")
def index():
    return render_template('web/index.html', version=config.VERSION)

# get sidebar menu configs
@app.route("/schemas/2007/categories.cat")
def sidebar():
    return app.send_static_file('categories.cat')

# bypass login
@app.route("/youtube/accounts/registerDevice", methods=['POST'])
@app.route("/youtube/accounts/applelogin1", methods=['POST'])
@app.route("/youtube/accounts/applelogin2", methods=['POST'])
def login_bypass():
    r2 = hashlib.md5(str(random.randint(1, 1000)).encode()).hexdigest()
    hmackr2 = hashlib.md5(str(random.randint(1, 1000)).encode()).hexdigest()
    auth = hashlib.md5(str(random.randint(1, 1000)).encode()).hexdigest()
    device_id_1 = hashlib.md5(str(random.randint(1, 1000)).encode()).hexdigest()
    device_key_1 = hashlib.md5(str(random.randint(1, 1000)).encode()).hexdigest()
    device_id_2 = hashlib.md5(str(random.randint(1, 1000)).encode()).hexdigest()
    device_key_2 = "ULxlVAAVMhZ2GeqZA/X1GgqEEIP1ibcd3S+42pkWfmk="

    # Returning all outputs
    return (
        f"r2={r2}\nhmackr2={hmackr2}\n\n"
        f"Auth={auth}\n\n"
        f"DeviceId={device_id_1}\nDeviceKey={device_key_1}\n\n"
        f"DeviceId={device_id_2}\nDeviceKey={device_key_2}"
    )

# --------------------------------------------- #

# images and videos
# TODO: cache images
# in testing
# --------------------------------------------- #

# fetches video from innertube.
@app.route("/getvideo/<video_id>")
def getvideo(video_id):

    if not config.MEDIUM_QUALITY:
        # Set mimetype since apple device don't recognized it.
        return Response(yt.hls_video_url(video_id), mimetype="application/vnd.apple.mpegurl")
    else:
        # 360p if enabled
        return redirect(yt.medium_quality_video_url(video_id), 307)

# --------------------------------------------- #

# api
# --------------------------------------------- #

# get channel info
@app.route("/feeds/api/channels/<channel_id>")
def search(channel_id):
    return get.channel_info(channel_id, request.url_root)

# featured videos
# 2 alternate routes for popular page and search results
@app.route("/feeds/api/standardfeeds/<regioncode>/<popular>")
@app.route("/feeds/api/standardfeeds/<popular>")
def frontpage(regioncode="US", popular=None):
    # app requested for region code
    return get.featured_videos(popular, regioncode, request.url_root)

# search for videos
@app.route("/feeds/api/videos")
def search_videos():
    query = request.args.get('q')
    return get.search_results(query, "video", request.url_root)

# search for channels
@app.route("/feeds/api/channels")
def channels():
    query = request.args.get('q')
    return get.search_results(query, "channel", request.url_root)

# video comments
# IDEA: filter the comments too?
@app.route("/api/videos/<videoid>/comments")
def comments(videoid):
    return get.comments(videoid, request.url_root)

# uploaded videos
@app.route("/feeds/api/users/<channel_id>/uploads")
def uploads(channel_id):
    return get.uploads(channel_id, request.url_root)

# get playlists
# TODO: get more video info since invidious simplified it.
@app.route("/feeds/api/users/<channel_id>/playlists")
def playlists(channel_id):
    return get.channel_playlists(channel_id, request.url_root)

# get playlist's video
# TODO: fix the damn thing
@app.route("/feeds/api/playlists/<playlist_id>")
def playlists_video(playlist_id):
    return get.playlist_videos(playlist_id, request.url_root)

# --------------------------------------------- #

# config
if __name__ == "__main__":
    if config.DEBUG:
        app.run(port=config.PORT, host="0.0.0.0", debug=True)
    else:
        serve(app, port=config.PORT, host="0.0.0.0")