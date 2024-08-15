import requests

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

    data = requests.post('https://www.youtube.com/youtubei/v1/player?key=AIzaSyB-63vPrdThhKuerbB2N_l7Kwwcxj6yUAc', json=json_data, headers=header_data).json()

    return data["streamingData"]['hlsManifestUrl']