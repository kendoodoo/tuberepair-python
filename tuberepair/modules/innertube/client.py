# hard-coded API Key, from youtube's private API
# no one bothered to change it. works with every client.
key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

player = 'https://www.youtube.com/youtubei/v1/player?key=' + key
browse = 'https://www.youtube.com/youtubei/v1/browse?key=' + key
search = 'https://www.youtube.com/youtubei/v1/search?key=' + key

# gl = region (example: US, UK, VN)
def Client(name, version, gl="US"):

	mock = {"client": {
      	"hl": "en",
      	"gl": gl,
      	"clientName": name,
    	"clientVersion": version
	}}

	return mock

# params: a "nice" way to spot trending topics by ID.
# google, i hate you.
def video_params(type):
    if type == "music":
        return "4gINGgt5dG1hX2NoYXJ0cw%3D%3D"
    if type == "gaming":
        return "4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D"
    if type == "movie":
        return "4gIKGgh0cmFpbGVycw%3D%3D"

# yes, i like to put it in a function.
def search_params(type):
	if type == "videos":
		return "EgIQAQ%3D%3D"
	if type == "playlists":
		return "CAASAhAD"
	if type == "channels":
		return "CAASAhAC"
	if type == "movies":
		return "CAASAhAE"

	# I'll probably put more, but the ID format sucks
	# MANUALLY.
