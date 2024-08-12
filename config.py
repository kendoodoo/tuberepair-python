# -- General -- #

# Pointed to what address
# your current ip if you're local, or domain
HOST = "https://cheese.kentest.net"

# HTTP connection protocol
# if your own instance is not secure go with http (default: https)
HTTP = "https"

# Set indivious instance
# remove the http:// or https://
URL = "inv.tux.pizza"

# Set port
# Anything around 1000-9000
PORT = "5000"

# Debug mode 
# recommended True if you want to fix the code and auto reload
DEBUG = True

# Spying on stuff
SPYING = True

# -- Custom functions ZONE! -- #

# Compress response
# Really helps squeezing it down
COMPRESS = True

# Number of featured videos (including categories)
# max: 50
FEATURED_VIDEOS = 15

# Number of search videos
# max: 20
SEARCHED_VIDEOS = 15

# Number of displayed comments
# max: 20
COMMENTS = 15

# Sort comments
# "newest", "popular"
SORT_COMMENTS = "popular"

# Thumbnail quality
# from 5 to 1 ascending: (5) 120x90, (4) 320x180, (3) 480x360, (2) 640x480, (1) 1280x720
# 3 and 2 recommended, 4 for lightweight loading
THUMBNAIL_QUALITY = 3