# -- DEV ZONE -- #
# You can change this to anything
import os
from modules import helpers
VERSION = "v0.0.6-beta-RC2"
# -------------- #

# -- General -- #

OSEnv = os.environ

# gets 360p by default is user doesn't provide a resolution
# NOTE: loads a ton faster
if "MEDIUM_QUALITY" in OSEnv:
    MEDIUM_QUALITY = helpers.string_to_bool(OSEnv["MEDIUM_QUALITY"])
else:
    MEDIUM_QUALITY = True


if "GET_ERROR_LOGGING" in OSEnv:
    GET_ERROR_LOGGING = helpers.string_to_bool(OSEnv["GET_ERROR_LOGGING"])
else:
    GET_ERROR_LOGGING = True

# resolution for DEFAULT HLS playback
# None, 144, 240, 360, 480, 720, 1080...
if "HLS_RESOLUTION" in OSEnv:
    HLS_RESOLUTION = int(OSEnv["HLS_RESOLUTION"])
else:
    HLS_RESOLUTION = 720

# Set indivious instance
# NOTE: for info fetching only right now.
# add http:// or https://

if "URL" in OSEnv:
    URL = OSEnv["URL"]
else:
    URL = "https://inv.nadeko.net"

if "PROXY" in OSEnv:
    helpers.setup_proxies(OSEnv["PROXY"])

# Max res to allow users
# Mainly to stop converting long numbers to strings.
# Always set this geater or equal to YouTubes Max res
# I don't recommend changing this.

if "RESMAX" in OSEnv and OSEnv["RESMAX"].isdigit():
    RESMAX = int(OSEnv["RESMAX"])
else:
    RESMAX = 36000

# Set port
# Anything around 1000-10000
# NOTE: set common ports so you can remember it.

if "PORT" in OSEnv:
    PORT = OSEnv["PORT"]
else:
    PORT = "4000"

# Debug mode 
# NOTE: recommended True if you want to fix the code and auto reload

if "DEBUG" in OSEnv:
    DEBUG = helpers.string_to_bool(OSEnv["DEBUG"])
else:
    DEBUG = True

# Spying on stuff
# NOTE: Don't judge people on their search lol
if "SPYING" in OSEnv:
    SPYING = helpers.string_to_bool(OSEnv["SPYING"])
else:
    SPYING = True

# Compress response
# NOTE: Really helps squeezing it down, about 80%. Won't affect potato PC that much.
if "SPYING" in OSEnv:
    COMPRESS = helpers.string_to_bool(OSEnv["SPYING"])
else:
    COMPRESS = True

# -- Custom functions -- #

# Number of featured videos (including categories)
# max: 50
if "FEATURED_VIDEOS" in OSEnv:
    FEATURED_VIDEOS = min(int(OSEnv["FEATURED_VIDEOS"]), 50)
else:
    FEATURED_VIDEOS = 20

# NO LONGER IN USE!
# Number of search videos
# max: 20
#if "SEARCHED_VIDEOS" in OSEnv:
#    SEARCHED_VIDEOS = min(int(OSEnv["SEARCHED_VIDEOS"]), 20)
#else:
#    SEARCHED_VIDEOS = 15

# Number of displayed comments
# max: 20
if "COMMENTS" in OSEnv:
    COMMENTS = min(int(OSEnv["COMMENTS"]), 20)
else:
    COMMENTS = 20

# Sort comments
# "newest", "popular"
if "SORT_COMMENTS" in OSEnv:
    SORT_COMMENTS = OSEnv["SORT_COMMENTS"]
else:
    SORT_COMMENTS = "popular"
