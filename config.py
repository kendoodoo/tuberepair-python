# -- DEV ZONE -- #
# You can change this to anything
VERSION = "v0.0.2-beta-1.5"
# -------------- #

# -- General -- #

# ///video/// #

# get 360p video instead of HLS
# NOTE: loads a ton faster
# True, False
MEDIUM_QUALITY = False

# resolution for HLS playback
# None, 144, 240, 360, 480, 720, 1080...
HLS_RESOLUTION = 480

# ////////// #

# Set indivious instance
# NOTE: for info fetching only right now.
# add http:// or https://
URL = "https://inv.tux.pizza"

# Set port
# Anything around 1000-10000
# NOTE: set common ports so you can remember it.
PORT = "3000"

# Debug mode 
# NOTE: recommended True if you want to fix the code and auto reload
DEBUG = True

# Spying on stuff
# NOTE: Don't judge people on their search lol
SPYING = True

# -- Custom functions -- #

# Number of featured videos (including categories)
# max: 50
FEATURED_VIDEOS = 20

# Number of search videos
# max: 20
SEARCHED_VIDEOS = 15

# Number of displayed comments
# max: 20
COMMENTS = 15

# Sort comments
# "newest", "popular"
SORT_COMMENTS = "popular"
