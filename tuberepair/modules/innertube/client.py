from requests_cache import CachedSession
from datetime import timedelta

from . import constants
from modules.client import helpers
import config

# cache videos.
video_cache = CachedSession('cache/videos', expire_after=timedelta(hours=config.CACHE_VIDEO), ignored_parameters=['key'], allowable_methods=['POST'], backend=config.backend)
# Video expires after 5 hours
session = video_cache

# TODO: add user agent spoofing. it might not work, but worth a shot.
# gl = region (example: US, UK, VN)
# Usage: Client(["WEB", "version"], "US")
def Client(config, gl="US"):

	mock = {"client": {
		"hl": "en",
		"gl": gl,
		"clientName": config[0],
		"clientVersion": config[1]
	}}

	return mock

# fetch the innertube API.
def get(url, json):
	data = session.post(url, json=json, proxies=helpers.proxies).json()
	return data

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

		# I'll probably put more, but the ID format sucks
		# MANUALLY.