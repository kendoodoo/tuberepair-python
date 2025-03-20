# TODO: split this thing
import requests_cache, re, config
from datetime import timedelta
from modules import helpers

# NOTE: check them first
from .innertube import client, handler
from .innertube.client import Client

# Video expires after 5 hours
session = requests_cache.CachedSession('cache/videos', expire_after=timedelta(hours=4), ignored_parameters=['key'], allowable_methods=('POST'), backend=config.backend)

# Get HLS URL via innertube and fetch the file, then filter to fix auto quality playback error
# SpaceSaver.
def data_to_hls_url(data, res=None):
    # get video's m3u8 to process it.
    stream = data["streamingData"]["hlsManifestUrl"]
    data = session.get(stream, proxies=helpers.proxies).text

    # spliting to... split the code for readability.
    return handler.misc.hls_quality_split(data, res)

def hls_video_url(video_id, res=None):
    # using IOS client since Apple invented HLS, duh.
    json_data = {
        "videoId": video_id,
        "context": Client("IOS", "19.16.3")
    }
    
    # fetch innertube
    data = session.post(client.player, json=json_data, proxies=helpers.proxies).json()
    return data_to_hls_url(data, res)

# experimental: client side video fetching.
# i think we should let regex do this on client-side.
def data_to_medium_url(data):
    return data["streamingData"]['formats'][0]['url']

# 360p
# for the kids who begged for this, here you go...
def medium_quality_video_url(video_id):

    json_data = {
        # This can play copyrighted videos. See https://github.com/tombulled/innertube/issues/76.
        "params": '8AEB',
        "videoId": video_id,
        "context": Client("ANDROID", "19.17.34")
    }

    # fetch the API.
    data = session.post(client.player, json=json_data, proxies=helpers.proxies).json()

    # i'm lazy. again.
    return data_to_medium_url(data)

# You know.
def trending_feeds(region="US", type=""):

    resp_json = []

    json_data = {
      "browseId": "FEtrending",
      "context": Client("WEB", "2.20230728.00.00", region)
    }

    # SEND TO YOUTUBE IMMEDIATELY
    data = session.post(client.browse, json=json_data).json()
    init = data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']

    # contents at item #3 (3 starting from 0), is intentional
    # 0 = 'is sponsored?'
    # 1 = '2 random videos'
    # 2 = 'shorts'
    video_items = init['contents'][3]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items']

    # TODO: add a invidious fallback for certain cases of failure
    for x in video_items:
      video = x['videoRenderer']
      # return in dict
      resp_json.append(dict(

        video_id=video['videoId'],
        channel_id=video['ownerText']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId'],
        channel_name=video['ownerText']['runs'][0]['text'],
        title=video['title']['runs'][0]['text'],
        # hottest fix on earth. 
        # TODO: put KeyError to jail.
        description=(video['descriptionSnippet']['runs'][0]['text'] if 'descriptionSnippet' in video else ''),
        views=handler.views(video['viewCountText']['simpleText'] if 'viewCountText' in video else 0),
        length=handler.to_seconds(video['lengthText']['simpleText'])

      ))

    return resp_json

def search(query, type="videos"):
    json_data = {
        "query": str(query),
        "params": client.search_params(type),
        "context": Client("WEB", "2.20230728.00.00")
    }

    data = requests.post(client.search, json=json_data).json()
    init = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

    for x in video_items:
      video = x['videoRenderer']

      # this has been in my head for 2 months, and a quick google search solves it.
      resp_json.append(dict(

        video_id=video['videoId'],
        channel_id=video['ownerText']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId'],
        channel_name=video['ownerText']['runs'][0]['text'],
        title=video['title']['runs'][0]['text'],
        description='No descriptions provided.',
        views=video['viewCountText']['simpleText'],
        published=video['publishedTimeText']['simpleText']

      ))


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
        data = session.post(client.browse, json=json_data).json()

        return {
            "name": data['header']['pageHeaderRenderer']['pageTitle'],
            "channel_id": data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['endpoint']['browseEndpoint']['browseId'],
            "profile_picture": data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['image']['decoratedAvatarViewModel']['avatar']['avatarViewModel']['image']['sources'][0]['url'],
            "subscribers": handler.subscribers(data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content'])
        }