# incase you used one of those files.
import config_env
# Redis
from requests_cache import RedisCache

# -- DEV ZONE -- #
# You can change this to anything.
VERSION = "v0.0.8-beta"
# -------------- #

# TODO: make this less of a mess.

# -- General -- #

# gets 360p by default is user doesn't provide a resolution
# NOTE: loads a ton faster
MEDIUM_QUALITY = True

# Use innertube
# Directly the YouTube Private API!
USE_INNERTUBE = True

# resolution for DEFAULT HLS playback
# None, 144, 240, 360, 480, 720, 1080...
HLS_RESOLUTION = 720

# Use invidious
# NOTE: for video fetching, in case of emergency.
# add http:// or https://
URL = "https://invidious.nerdvpn.de"

# Spying on stuff
# NOTE: Don't judge people on their search lol
SPYING = True

# Set amount of featured videos.
# NOTE: to cut bandwidth or load, either way.
FEATURED_VIDEOS = 20

# Set amount of comments
# For each continuation.
COMMENTS = 20

# Sort comments by...
# "newest", "popular"
SORT_COMMENTS = "popular"

# -- Misc -- #

# Set port
# Anything around 1 to 65000-ish
# NOTE: set common ports so you can remember it. like 3000, 4000, 8000...
PORT = 2000

# Debug mode
# NOTE: ALWAYS turn this on if you want to report bugs.
DEBUG = True

# TODO: explain me this too. what is this?
CLIENT_TEST = False

# Compress XML responses by GZIP
# NOTE: Not resource intensive.
COMPRESS = True

# Set maximum resolution to use in URL.
# TODO: explain me this.
RESMAX = 36000

# TODO: overlapping "SPYING"???
GET_ERROR_LOGGING = True

# ---------- #

# If you know what you're doing, go ahead.
# (so cliche...)

# -- database -- #

# cache for info
# (in hours)
CACHE_INFO = 1

# cache for videos
# NOTE: google will automatically remove the link in 5 hours
# (in hours)
CACHE_VIDEO = 4

# Use REDIS? NO THANKS.
# You could use it tho...
USE_REDIS = False

# TODO: put it somewhere else...
if USE_REDIS:
    backend = RedisCache(host=OSEnv["REDIS_HOST"], port=OSEnv["REDIS_PORT"])

# TODO: explain me this. what is this?
backend = 'sqlite'

# --------- #