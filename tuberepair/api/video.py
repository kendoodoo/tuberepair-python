# imports
from flask import Blueprint, Flask, request, redirect, render_template, Response, g
from functools import wraps

# custom ones
from modules.client import get, helpers
from modules.client.logs import print_with_seperator
from modules import yt
import config

video = Blueprint("video", __name__)

# added a flask decorator to make life easier
def sanitize(f):

    @wraps(f)
    def log(*args, **kwargs):

        if type(kwargs.get('res', None)) == int:
            res = min(max(res, 144), config.RESMAX)

        return f(*args, **kwargs)
    return log

# featured videos
# 2 alternate routes for popular page and search results
@sanitize
def frontpage(regioncode="US", popular=None, res=''):

    # Will be used for checking Classic
    user_agent = request.headers.get('User-Agent')
    print(user_agent)

    # print logs if enabled
    if config.SPYING == True:
        print_with_seperator("Region code: " + regioncode)

    if helpers.classic(user_agent):
        # get template
        return get.template('classic/featured.jinja2',{
            'data': yt.trending_feeds(),
            'unix': get.unix
        })
    else:
        # Google YT
        return render_template('featured.jinja2', data=yt.trending_feeds(), unix=get.unix)

    return get.error()

# search for videos
# TODO: ditch.
def search_videos(res=''):

    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)

    url = request.url_root + str(res)
    currentPage, next_page = helpers.process_start_index(request)

    user_agent = request.headers.get('User-Agent')

    search_keyword = request.args.get('q').replace(" ", "%20")

    if not search_keyword:
        return get.error()

    # print logs if enabled
    if config.SPYING == True:
        print_with_seperator('Searched: ' + search_keyword)

    # q and page is already made, so lets hand add it
    query = f'q={search_keyword}&type=video&page={currentPage}'

    # If we have orderby, turn it into invidious friendly parameters
    # Else ignore it
    orderby = request.args.get('orderby')
    if orderby in helpers.valid_search_orderby:
        query += f'&sort={helpers.valid_search_orderby[orderby]}'

    # If we have time, turn it into invidious friendly parameters
    # Else ignore it
    time = request.args.get('time')
    if time in helpers.valid_search_time:
        query += f'&date={helpers.valid_search_time[time]}'

    # If we have duration, turn it into invidious friendly parameters
    # Else ignore it
    duration = request.args.get('duration')
    if duration in helpers.valid_search_duration:
        query += f'&duration={helpers.valid_search_duration[duration]}'

    # If we have captions, turn it into invidious friendly parameters
    # Else ignore it
    # NOTE: YouTube 1.1.0 app only supports subtitles in the search
    caption = request.args.get('caption')
    if type(caption) == str and caption.lower() == 'true':
        query += '&features=subtitles'

    # Santize and stitch
    query = query.replace('&', '&amp;')

    # search by videos
    data = get.fetch(f"{config.URL}/api/v1/search?{query}")

    if not data:
        next_page = None

    # classic tube check
    if helpers.classic(user_agent):
        return get.template('classic/search.jinja2',{
            'data': data,
            'unix': get.unix,
            'url': url,
            'next_page': next_page
        })
    else:
        return get.template('search_results.jinja2',{
            'data': data,
            'unix': get.unix,
            'url': url,
            'next_page': next_page
        })

# video's comments
# IDEA: filter the comments too?
def comments(videoid, res=''):

    # Clamp Res
    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)

    url = request.url_root + str(res)

    # this shit is so messy, ditchchhhhhh
    continuation_token = request.args.get('continuation') and '&amp;continuation=' + request.args.get('continuation') or ''
    # fetch invidious comments api
    data = get.fetch(f"{config.URL}/api/v1/comments/{videoid}?sortby={config.SORT_COMMENTS}{continuation_token}")

    if data:
        # NOTE: No comments sometimes returns {'error': 'Comments not found.'}
        if 'error' in data:
            comments = None
        else:
            comments = data['comments']
        return get.template('comments.jinja2',{
            'data': comments,
            'unix': get.unix,
            'url': url,
            'continuation': 'continuation' in data and data['continuation'] or None,
            'video_id': videoid
        })

    return get.error()

if (config.USE_INNERTUBE):
    # fetches video from innertube.
    @video.route("/getvideo/<video_id>")
    @video.route("/<int:res>/getvideo/<video_id>")
    def getvideo(video_id, res=None):
        if res is not None or config.MEDIUM_QUALITY is False:

            # Clamp Res
            if type(res) == int:
                res = min(max(res, 144), config.RESMAX)

            # Set mimetype since videole device don't recognized it.
            return Response(yt.video.hls_video_url(video_id, res), mimetype="application/vnd.apple.mpegurl")

        # 360p if enabled
        return redirect(yt.video.medium_quality_video_url(video_id), 307)
else:
    # fetches video from invidious.
    @video.route("/getvideo/<video_id>")
    @video.route("/<int:res>/getvideo/<video_id>")
    def getvideo(video_id, res = None):
        data = get.fetch(f"{config.URL}/api/v1/videos/{video_id}")
        '''
        if res is not None or config.MEDIUM_QUALITY is False:

            # Clamp Res
            if type(res) == int:
                res = min(max(res, 144), config.RESMAX)

            for adaptive in data['adaptiveFormats']:

            return Response(yt.hls_video_url(video_id, res), mimetype="application/vnd.apple.mpegurl")
        '''
        # 360p if enabled
        # TODO: Fix resoution not working.
        return redirect(data['formatStreams'][0]['url'], 307)

def get_suggested(video_id, res=''):

    data = get.fetch(f"{config.URL}/api/v1/videos/{video_id}")

    url = request.url_root + str(res)
    user_agent = request.headers.get('User-Agent')

    if data:
        if 'error' in data:
            data = None
        else:
            data = data['recommendedVideos']
        # classic tube check
        if helpers.classic(user_agent):
            return get.template('classic/search.jinja2',{
                'data': data,
                'unix': get.unix,
                'url': url,
                'next_page': None
            })

        return get.template('search_results.jinja2',{
            'data': data,
            'unix': get.unix,
            'url': url,
            'next_page': None
        })
    return get.error()

# worse than hell, but it works
def assign(path, func):
    bprint = video
    # saves a ton of unnecessary
    bprint.add_url_rule(path, view_func=func)

    # here's your res, kevin
    bprint.add_url_rule("/<int:res>" + path, view_func=func)

# paths for trending feeds
assign("/feeds/api/standardfeeds/<regioncode>/<popular>", frontpage)
assign("/feeds/api/standardfeeds/<popular>", frontpage)
# paths for search videos
assign("/feeds/api/videos/", search_videos)
# paths for video comments
assign("/api/videos/<videoid>/comments", comments)
assign("/feeds/api/videos/<videoid>/comments", comments)
# get video
assign("/getvideo/<video_id>", getvideo)
# get related videos
assign("/feeds/api/videos/<video_id>/related", get_suggested)