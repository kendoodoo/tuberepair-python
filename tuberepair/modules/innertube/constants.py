# Yes, I copied this from youtubei.js. CONSTANTS 4ever.
# Kind of shitty.

base_url = 'https://www.youtube.com/youtubei/v1/'

# hard-coded API Key, from youtube's private API
# no one bothered to change it. works with every client.
key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

player = base_url + 'player?key=' + key
browse = base_url + 'browse?key=' + key
search = base_url + 'search?key=' + key

class client:
	WEB = ["WEB", "2.20230728.00.00"]
	WEB_KIDS = ["WEB_KIDS", "2.20230111.00.00"]
	IOS = ["IOS", "19.16.3"]
	ANDROID = ["ANDROID", "19.17.34"]

# params: a "nice" way to spot trending topics by ID.
# google, i hate you.
class param:
	def video(type):
		if type == "music":
			return "4gINGgt5dG1hX2NoYXJ0cw%3D%3D"
		if type == "gaming":
			return "4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D"
		if type == "movie":
			return "4gIKGgh0cmFpbGVycw%3D%3D"

	def search(type):
		if type == "videos":
			return "EgIQAQ%3D%3D"
		if type == "playlists":
			return "CAASAhAD"
		if type == "channels":
			return "CAASAhAC"
		if type == "movies":
			return "CAASAhAE"
	
	channel_info = "EgZzaG9ydHPyBgUKA5oBAA%3D%3D"

		# I'll probably put more, but the ID format sucks
		# MANUALLY.