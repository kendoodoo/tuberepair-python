# Version whatever...
import signal
from flask import Flask, g
from flask_compress import Compress
import config
from waitress import serve

# seperated apis
from api.static import static
from api.playlist import playlist
from api.video import video
from api.channel import channel

# log
from modules.client import logs

if config.CLIENT_TEST:
    from api.client_videos import client_videos

# init
# load version text
logs.version(config.VERSION)
app = Flask(__name__)

# HACK: remove the slash at the end. GLOBALLY.
# checkmate, kevin!
app.url_map.strict_slashes = False

# trim jinja2 whitespace
# just a little fine tuning
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# register seperate paths
app.register_blueprint(static)
app.register_blueprint(playlist)
app.register_blueprint(video)
app.register_blueprint(channel)
if config.CLIENT_TEST:
    app.register_blueprint(client_videos)
    
# use compression to load faster via client
if config.COMPRESS:
    compress = Compress(app)

# config
if __name__ == "__main__":
    # Docker shenanigans
    signal.signal(signal.SIGTERM, lambda *args: exit())

    # TODO: what's the point of disabling DEBUG?
    if config.DEBUG:
        app.run(port=config.PORT, host="0.0.0.0", debug=True)
    else:
        serve(app, port=config.PORT, host="0.0.0.0")