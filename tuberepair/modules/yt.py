# NOTE: check them first
from .innertube import client, handler, constants
from .innertube.client import Client

# TBH, I don't even know how to use python.
class video:
    # Get HLS URL via innertube and fetch the file, then filter to fix auto quality playback error
    # SpaceSaver.
    def data_to_hls_url(data, res=None):
        # get video's m3u8 to process it.
        stream = data["streamingData"]["hlsManifestUrl"]
        data = client.get(stream, proxies=helpers.proxies).text

        # spliting to... split the code for readability.
        return handler.misc.hls_quality_split(data, res)

    def hls_video_url(video_id, res=None):
        # using IOS client since Apple invented HLS.
        json_data = {
            "videoId": video_id,
            "context": Client(constants.IOS)
        }
        
        # fetch innertube
        data = client.post(client.player, json_data)
        return data_to_hls_url(data, res)

    # experimental: client side video fetching.
    def data_to_medium_url(data):
        return data["streamingData"]['formats'][0]['url']

    # 360p
    # for the kids who begged for this, here you go...
    def medium_quality_video_url(video_id):

        json = {
            # This can play copyrighted videos. 
            # See https://github.com/tombulled/innertube/issues/76.
            "params": '8AEB',
            "videoId": video_id,
            "context": Client(constants.ANDROID)
        }

        # fetch the API.
        data = client.post(constants.player, json)

        # i'm lazy. again.
        return video.data_to_medium_url(data)

# You know.
def trending_feeds(region="US", type=""):

    resp_json = []

    json = {
      "browseId": "FEtrending",
      "context": Client(constants.WEB, region)
    }

    # SEND TO YOUTUBE IMMEDIATELY
    data = client.post(constants.browse, json)
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
    json = {
        "query": str(query),
        "params": constant.param.search(type),
        "context": Client(constants.WEB)
    }

    data = requests.post(constants.search, json)
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

def simple_channel_info(id):

    json = {
        "context": Client(constants.WEB),
        "params": "EgZzaG9ydHPyBgUKA5oBAA%3D%3D",
        "browseId": id
    }

    # fetch the API.
    data = client.post(constants.browse, json)

    return {
        "name": data['header']['pageHeaderRenderer']['pageTitle'],
        "channel_id": data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['endpoint']['browseEndpoint']['browseId'],
        "profile_picture": data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['image']['decoratedAvatarViewModel']['avatar']['avatarViewModel']['image']['sources'][0]['url'],
        "subscribers": handler.subscribers(data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['metadata']['contentMetadataViewModel']['metadataRows'][1]['metadataParts'][0]['text']['content'])
    }