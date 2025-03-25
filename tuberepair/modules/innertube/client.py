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
def post(url, json):
	data = session.post(url, json=json, proxies=helpers.proxies).json()
	return data

# fetch the innertube API.
def get(url, json):
	data = session.get(url, json=json, proxies=helpers.proxies).json()
	return data