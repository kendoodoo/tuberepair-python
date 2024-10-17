import requests, re
import requests_cache
from datetime import timedelta
import ua_generator

import config

# Videos expires after 5 hours, so you don't have to worry.
session = requests_cache.CachedSession('cache/videos', expire_after=timedelta(hours=4), ignored_parameters=['key'])

# hard-coded API Key, so no limit at all.
api_key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

# Get HLS URL via youtubei and fetch the file, then filter to fix low quality playback error
# Much thanks for SpaceSaver.
def hls_video_url(video_id, res=None):

    # generate random user agent to spoof
    #
    ios_user_agent = str(ua_generator.generate(platform='ios'))
    header_data = {
        "User-Agent": ios_user_agent,
        "Referer": "https://m.youtube.com/"
    }

    # using IOS client since Apple invented HLS, duh.
    json_data = {
        "context": {"client": {
            "clientName": "IOS",
            "clientVersion": "19.16.3",
            "visitorData": "CgtfVHB0eHw4PIBAREiEgHg%3D%3D"
        }},
        "videoId": video_id
    }
    
    # fetch innertube
    data = session.post('https://www.youtube.com/youtubei/v1/player?key=' + api_key, json=json_data, headers=header_data).json()
    # get video's m3u8 to process it.
    panda = session.get(data["streamingData"]["hlsManifestUrl"]).text.split("\n")

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

# play 360p
# for the kids who begged for this, here you go...
def medium_quality_video_url(video_id):

    # changing header to spoof
    misc_user_agent = str(ua_generator.generate(device='desktop', platform='windows', browser='chrome'))
    header_data = {
        "User-Agent": misc_user_agent
    }

    json_data = {
        "context": {"client": {
            "clientName": "ANDROID",
            "clientVersion": "19.17.34"
        }},
        # This can play copyrighted videos.
        "params": '8AEB',
        "videoId": video_id
    }

    # fetch the API.
    data = session.post('https://www.youtube.com/youtubei/v1/player?key=' + api_key, json=json_data, headers=header_data).json()

    # i'm lazy. again.
    return data["streamingData"]['formats'][0]['url']

def channel_playlists():

    # changing header to spoof
    misc_user_agent = str(ua_generator.generate(device='desktop', platform='windows', browser='chrome'))
    header_data = {
        "User-Agent": misc_user_agent
    }

    json_data = {
        "context": {"client": {
            "clientName": "TVHTML5_CAST",
            "clientVersion": "1.1"
        }},
        "browseId": "VL" + "PLnMc0DcIgIXI6-K3FSfc08CKDw5FObaDP"
    }

    # fetch the API.
    data = requests.post('https://www.youtube.com/youtubei/v1/browse?key=' + api_key, json=json_data, headers=header_data).json()

    # i'm lazy. again.
    return data

def channel_info():

    # changing header to spoof
    misc_user_agent = str(ua_generator.generate(device='desktop', platform='windows', browser='chrome'))
    header_data = {
        "User-Agent": misc_user_agent
    }

    json_data = {
        "context": {
            'client': {
                'hl': 'en',
                'gl': 'US',
                'clientName': 'ANDROID',
                'clientVersion': '19.17.34'
            }
        },
        "browseId": "UCrEKPrJOkTbaOxeZJ8q6Dew"
    }

    # fetch the API.
    data = requests.post('https://www.youtube.com/youtubei/v1/browse?key=' + api_key, json=json_data, headers=header_data).json()

    # i'm lazy. again.
    return data
