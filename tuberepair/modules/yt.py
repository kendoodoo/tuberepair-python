import requests, re
import requests_cache
from datetime import timedelta

import config
from modules import helpers, get

# Videos expires after 5 hours, so you don't have to worry.
session = requests_cache.CachedSession('cache/videos', expire_after=timedelta(hours=4), ignored_parameters=['key'])

# hard-coded API Key, from youtube's private API
api_key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

# Get HLS URL via innertube and fetch the file, then filter to fix low quality playback error
# Much thanks for SpaceSaver.
def hls_video_url(video_id, res=None):

    # using IOS client since Apple invented HLS
    json_data = {
        "context": {"client": {
            "clientName": "IOS",
            "clientVersion": "19.16.3"
        }},
        "videoId": video_id
    }
    
    # fetch innertube
    data = session.post('https://www.youtube.com/youtubei/v1/player?key=' + api_key, json=json_data, proxies=helpers.proxies).json()
    # get video's m3u8 to process it.
    panda = session.get(data["streamingData"]["hlsManifestUrl"], proxies=helpers.proxies).text.split("\n")

    # regex filter
    formatfilter = re.compile(r"^#EXT-X-STREAM-INF:BANDWIDTH=(?P<bandwidth>\d+),CODECS=\"(?P<codecs>[^\"]+)\",RESOLUTION=(?P<width>\d+)x(?P<height>\d+),FRAME-RATE=(?P<fps>\d+),VIDEO-RANGE=(?P<videoRange>[^,]+),AUDIO=\"(?P<audioGroup>[^\"]+)\"(,SUBTITLES=\"(?P<subGroup>[^\"]+)\")?")
    vertical = None
    maxRes = 0
    wanted_resolution = res and type(res) == int and min(max(res, 144), config.RESMAX) or config.HLS_RESOLUTION or 360
    # doesn't bother to explain the code, sooo...
    # TODO: explain the thing, lazer eyed cat.
    for x in range(len(panda)):
        line = panda[x]
        match = formatfilter.match(line)

        # dude
        if not match:
            continue
        
        # continue if codecs is not compatible (or matched?)
        if not match.group("codecs").startswith("avc"):
            panda[x] = ""
            panda[x+1] = ""
            continue
        
        # reject framerates over 30
        if int(match.group("fps")) > 30:
            panda[x] = ""
            panda[x+1] = ""
            continue
        
        if vertical is None:
            vertical = int(match.group("height")) > int(match.group("width"))
        res = 0

        # match vertical with width, because higher
        if vertical:
            res = int(match.group("width"))
        else:
            res = int(match.group("height"))

        # if resolution bigger than the expected height, skip
        if res > wanted_resolution:
            panda[x] = ""
            panda[x+1] = ""
            continue

        if res > maxRes:
           maxRes = res

    for x in range(len(panda)):
        line = panda[x]
        match = formatfilter.match(line)

        if not match:
            continue
        res = 0

        if vertical:
            res = int(match.group("width"))
        else:
            res = int(match.group("height"))

        if res < maxRes:
            panda[x] = ""
            panda[x+1] = ""

    panda = "\n".join(panda)
    return panda

# 360p (SD)
def medium_quality_video_url(video_id):

    json_data = {
        "context": {"client": {
            "clientName": "ANDROID",
            "clientVersion": "19.17.34"
        }},
        # This can play copyrighted videos.
        # See https://github.com/tombulled/innertube/issues/76
        "params": 'CgIQBg==',
        "videoId": video_id
    }

    # fetch the API.
    data = session.post('https://www.youtube.com/youtubei/v1/player?key=' + api_key, json=json_data, proxies=helpers.proxies).json()

    return data["streamingData"]['formats'][0]['url']

class metadata:

    def simple_channel_info(id):

        json_data = {
            "context": {
                'client': {
                    'clientName': 'WEB',
                    'clientVersion': '2.20240814.00.00'
                }
            },
            "params": "EgZzaG9ydHPyBgUKA5oBAA%3D%3D",
            "browseId": id
        }

        # fetch the API.
        data = session.post('https://www.youtube.com/youtubei/v1/browse?key=' + api_key, json=json_data).json()

        # i'm lazy. again.
        return {
            "name": data['header']['pageHeaderRenderer']['pageTitle'],
            "channel_id": data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['endpoint']['browseEndpoint']['browseId'],
            "profile_picture": data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['image']['decoratedAvatarViewModel']['avatar']['avatarViewModel']['image']['sources'][0]['url'],
            "subscribers": get.subscribers(data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content'])
        }