import requests, re
import requests_cache
from datetime import timedelta

session = requests_cache.CachedSession('cache/videos', expire_after=timedelta(hours=4), ignored_parameters=['key'])

api_key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'



def hls_video_url(video_id):

    header_data = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/98.2  Mobile/15E148 Safari/605.1.15"
    }

    json_data = {
        "context": {"client": {
            "clientName": "IOS",
            "clientVersion": "19.16.3"
        }},
        "videoId": video_id
    }
    
    data = requests.post('https://www.youtube.com/youtubei/v1/player?key=' + api_key, json=json_data, headers=header_data).json()
    panda = requests.get(data["streamingData"]["hlsManifestUrl"]).text.split("\n")
    formatfilter = re.compile(r"^#EXT-X-STREAM-INF:BANDWIDTH=(?P<bandwidth>\d+),CODECS=\"(?P<codecs>[^\"]+)\",RESOLUTION=(?P<width>\d+)x(?P<height>\d+),FRAME-RATE=(?P<fps>\d+),VIDEO-RANGE=(?P<videoRange>[^,]+),AUDIO=\"(?P<audioGroup>[^\"]+)\"(,SUBTITLES=\"(?P<subGroup>[^\"]+)\")?")
    vertical = None
    maxRes = 0
    for x in range(len(panda)):
        line = panda[x]
        match = formatfilter.match(line)
        if not match:
            continue
        if not match.group("codecs").startswith("avc"):
            panda[x] = ""
            panda[x+1] = ""
            continue
        if int(match.group("fps")) > 30:
            panda[x] = ""
            panda[x+1] = ""
            continue
        if vertical is None:
            vertical = int(match.group("height")) > int(match.group("width"))
        res = 0
        if vertical:
            res = int(match.group("width"))
        else:
            res = int(match.group("height"))
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
def medium_quality_video_url(video_id):

    header_data = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10553"
    }

    json_data = {
        "context": {"client": {
            "clientName": "TVLITE",
            "clientVersion": "2"
        }},
        "videoId": video_id
    }

    data = session.post('https://www.youtube.com/youtubei/v1/player?key=' + api_key, json=json_data, headers=header_data).json()

    return data["streamingData"]['formats'][0]['url']
