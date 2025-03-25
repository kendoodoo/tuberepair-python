import requests

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