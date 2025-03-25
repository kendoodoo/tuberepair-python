# imports
from flask import Blueprint, Flask, request, redirect, render_template, Response
from functools import wraps

# custom ones
from modules.client import get, helpers
from modules.client.logs import print_with_seperator
from modules import yt
import config

video = Blueprint("video", __name__)

# featured videos
# 2 alternate routes for popular page and search results
def frontpage(regioncode="US", popular=None, res=''):
    
    url = request.url_root

    if type(res) == int:
        res = min(max(res, 144), config.RESMAX)

    # Will be used for checking Classic
    user_agent = request.headers.get('User-Agent')
    print(user_agent)

    # print logs if enabled
    if config.SPYING == True:
        print_with_seperator("Region code: " + regioncode)

    if helpers.user_agent(user_agent):
        # get template
        return get.template('classic/featured.jinja2',{
            'data': yt.trending_feeds(),
            'unix': get.unix,
            'url': url
        })
    else:
        # Google YT
        return get.template('featured.jinja2',{
            'data': yt.trending_feeds(),
            'unix': get.unix,
            'url': url
        })

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

    search_keyword = request.args.get('q')

    if not search_keyword:
        return get.error()

    # print logs if enabled
    if config.SPYING == True:
        print_with_seperator('Searched: ' + search_keyword)

    # remove space character
    search_keyword = search_keyword.replace(" ", "%20")

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
    if helpers.user_agent(user_agent):
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
@video.route("/api/videos/<videoid>/comments")
@video.route("/<int:res>/api/videos/<videoid>/comments")
@video.route("/feeds/api/videos/<videoid>/comments")
@video.route("/<int:res>/feeds/api/videos/<videoid>/comments")
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

@video.route("/feeds/api/videos/<video_id>/related")
@video.route("/<int:res>/feeds/api/videos/<video_id>/related")
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
        if helpers.user_agent(user_agent):
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

# worse than hell, but works

# paths for trending feeds
video.add_url_rule("/feeds/api/standardfeeds/<regioncode>/<popular>", view_func=frontpage)
video.add_url_rule("/feeds/api/standardfeeds/<popular>", view_func=frontpage)
video.add_url_rule("/<int:res>/feeds/api/standardfeeds/<regioncode>/<popular>", view_func=frontpage)
video.add_url_rule("/<int:res>/feeds/api/standardfeeds/<popular>", view_func=frontpage)

# paths for search videos
video.add_url_rule("/feeds/api/videos", view_func=search_videos)
video.add_url_rule("/feeds/api/videos/", view_func=search_videos)
video.add_url_rule("/<int:res>/feeds/api/videos", view_func=search_videos)
video.add_url_rule("/<int:res>/feeds/api/videos/", view_func=search_videos)