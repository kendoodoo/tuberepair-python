# Version v0.0.1 (beta-3.5)
import signal
from flask import Flask
from flask_compress import Compress
import config
from waitress import serve

# seperated apis
from api.static import static
from api.playlist import playlist
from api.video import video
from api.channel import channel
from modules import logs

if config.CLIENT_TEST:
    from api.client_videos import client_videos

# init
# Load version text
logs.version(config.VERSION)
app = Flask(__name__)

# register seperate paths
app.register_blueprint(static)
app.register_blueprint(playlist)
app.register_blueprint(video)
app.register_blueprint(channel)
if config.CLIENT_TEST:
    app.register_blueprint(client_videos)

# use compression to load faster
if config.COMPRESS:
    compress = Compress(app)

# Catch sigterm for docker
def catch_docker_stop(*args):
    exit()

# config
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, catch_docker_stop)
    if config.DEBUG:
        app.run(port=config.PORT, host="0.0.0.0", debug=True)
    else:
        serve(app, port=config.PORT, host="0.0.0.0")