# Version v0.0.1 (beta-3.5)
from flask import Flask, request, redirect, send_file, Response
from flask_compress import Compress
from uuid import uuid4

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

# get sidebar menu configs
@app.route("/schemas/2007/categories.cat")
def sidebar():
    return app.send_static_file('categories.cat')

# bypass login
@app.route("/youtube/accounts/registerDevice", methods=['POST'])
def login_bypass():
    # return random key
    key = uuid4().hex
    return f"DeviceId={key}\nDeviceKey={key}"

# --------------------------------------------- #

# images and videos
# in testing
# --------------------------------------------- #

# fetches video from innertube.
@app.route("/getvideo/<video_id>")
def getvideo(video_id):
    streams = yt.hls_video(video_id)
    return Response(streams, mimetype="application/vnd.apple.mpegurl")

# --------------------------------------------- #

# api
# --------------------------------------------- #

# get channel info
@app.route("/feeds/api/channels/<channel_id>")
def search(channel_id):
    return get.channel_info(channel_id)

# featured videos
# 2 alternate routes for popular page and search results
@app.route("/feeds/api/standardfeeds/<regioncode>/<popular>")
@app.route("/feeds/api/standardfeeds/<popular>")
def frontpage(regioncode="US", popular=None):
    # app requested for region code
    return get.featured_videos(popular, regioncode)

# search for videos
@app.route("/feeds/api/videos")
def search_videos():
    query = request.args.get('q')
    return get.search_results(query, "video")

# search for channels
@app.route("/feeds/api/channels")
def channels():
    query = request.args.get('q')
    return get.search_results(query, "channel")

# video comments
@app.route("/api/videos/<videoid>/comments")
def comments(videoid):
    return get.comments(videoid)

# uploaded videos
@app.route("/feeds/api/users/<channel_id>/uploads")
def uploads(channel_id):
    return get.uploads(channel_id)

# get playlists
@app.route("/feeds/api/users/<channel_id>/playlists")
def playlists(channel_id):
    return get.channel_playlists(channel_id)

# get playlist's video
@app.route("/feeds/api/playlists/<playlist_id>")
def playlists_video(playlist_id):
    return get.playlist_videos(playlist_id)

# --------------------------------------------- #

# config
if __name__ == "__main__":
    app.run(port=config.PORT, host="0.0.0.0", debug=config.DEBUG)
