from modules import get
from flask import Blueprint, Flask, request, redirect, render_template, Response
import config
from modules.logs import text
from modules import yt

video = Blueprint("video", __name__)

def error():
    return "",404

# featured videos
# 2 alternate routes for popular page and search results
@video.route("/feeds/api/standardfeeds/<regioncode>/<popular>")
@video.route("/feeds/api/standardfeeds/<popular>")
@video.route("/<int:res>/feeds/api/standardfeeds/<regioncode>/<popular>")
@video.route("/<int:res>/feeds/api/standardfeeds/<popular>")
def frontpage(regioncode="US", popular=None, res=''):
    url = request.url_root + str(res) 
    # trending videos categories
    # the menu got less because of youtube removing it.
    apiurl = config.URL + "/api/v1/trending?region=" + regioncode
    if popular == "most_popular_Film":
        apiurl = f"{config.URL}/api/v1/trending?type=Movies&region={regioncode}"
    if popular == "most_popular_Games":
        apiurl = f"{config.URL}/api/v1/trending?type=Gaming&region={regioncode}"
    if popular == "most_popular_Music":
        apiurl = f"{config.URL}/api/v1/trending?type=Music&region={regioncode}"    

    # fetch api from invidious
    data = get.fetch(apiurl)
    
    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if data:

        # print logs if enabled
        if config.SPYING == True:
            text("Region code: " + regioncode)

        # Classic YT path
        if popular == "recently_featured" or popular == "most_viewed" or popular == "top_rated":
            # get template
            return get.template('classic/featured.jinja2',{
                'data': data[:15],
                'unix': get.unix,
                'url': url
            })
        
        # Google YT
        return get.template('featured.jinja2',{
            'data': data[:config.FEATURED_VIDEOS],
            'unix': get.unix,
            'url': url
        })

    return error()

# search for videos
@video.route("/feeds/api/videos")
@video.route("/feeds/api/videos/")
@video.route("/<int:res>/feeds/api/videos")
@video.route("/<int:res>/feeds/api/videos/")
def search_videos(res=''):
    url = request.url_root + str(res)
    print("here", request.url_root)
    user_agent = request.headers.get('User-Agent')
    query = request.args.get('q')

    # remove space character
    search_keyword = query.replace(" ", "%20")
    
    # print logs if enabled
    if config.SPYING == True:
        text('Searched: ' + query)
    # search by videos
    data = get.fetch(f"{config.URL}/api/v1/search?q={search_keyword}&type=video")

    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if data:

        # classic tube check
        if "YouTube v1.0.0" in user_agent:
            return get.template('classic/search.jinja2',{
                'data': data[:config.SEARCHED_VIDEOS],
                'unix': get.unix,
                'url': url
            })

        return get.template('search_results.jinja2',{
            'data': data[:config.SEARCHED_VIDEOS],
            'unix': get.unix,
            'url': url
        })

    return error()

# video's comments
# IDEA: filter the comments too?
@video.route("/api/videos/<videoid>/comments")
@video.route("/<int:res>/api/videos/<videoid>/comments")
def comments(videoid, res=''):
    url = request.url_root + str(res) 
    # fetch invidious comments api
    data = get.fetch(f"{config.URL}/api/v1/comments/{videoid}?sortby={config.SORT_COMMENTS}")

    # Templates have the / at the end, so let's remove it.
    if url[-1] == '/':
        url = url[:-1]

    if data:

        return get.template('comments.jinja2',{
            'data': data['comments'],
            'unix': get.unix,
            'url': url
        })

    return error()
    
# fetches video from innertube.
@video.route("/getvideo/<video_id>")
@video.route("/<int:res>/getvideo/<video_id>")
def getvideo(video_id, res=None):
    if res is not None or config.MEDIUM_QUALITY is False:
        # Set mimetype since videole device don't recognized it.
        return Response(yt.hls_video_url(video_id, res), mimetype="application/vnd.apple.mpegurl")
    
    # 360p if enabled
    return redirect(yt.medium_quality_video_url(video_id), 307)