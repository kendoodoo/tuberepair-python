# -- DEV ZONE -- #
# You can change this to anything
VERSION = "v0.0.2-beta1"
# -------------- #

# -- General -- #

# get 360p video
# NOTE: loads a ton faster
MEDIUM_QUALITY = True

# Set indivious instance
# NOTE: for info fetching only right now.
# add http:// or https://
URL = "https://inv.tux.pizza"

# Set port
# Anything around 1000-10000
# NOTE: set common ports so you can remember it.
PORT = "4000"

# Rate limiting
# Useful if you're hosting it for dozens of people. To prevent spam.
RATE_LIMITING = False

# Debug mode 
# NOTE: recommended True if you want to fix the code and auto reload
DEBUG = True

# Spying on stuff
# NOTE: Don't judge people on their search lol
SPYING = True

# Compress response
# NOTE: Really helps squeezing it down, about 80%. Won't affect potato PC that much.
COMPRESS = True

# -- Custom functions -- #

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
