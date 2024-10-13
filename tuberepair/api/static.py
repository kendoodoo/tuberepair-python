from flask import Blueprint, request, redirect, send_file, render_template, Response
import config
from uuid import uuid4

static = Blueprint("static", __name__, static_folder="../static")

# static contents (sort of)
# --------------------------------------------- #

@static.route("/")
def index():
    return render_template('web/index.html', version=config.VERSION, medium=config.MEDIUM_QUALITY, hls=config.HLS_RESOLUTION)

@static.route("/hehe")
def sidebawr():
    return static.send_static_file('jeeezus.mp4')



# sidebar menu
@static.route("/schemas/2007/categories.cat")
def sidebar():
    return static.send_static_file('categories.cat')

# bypass login
# for youtube classic.
@static.route("/youtube/accounts/applelogin1", methods=['POST'])
def legacy_login_bypass():
    return f'''r2={uuid4().hex}\nhmackr2={uuid4().hex}'''

@static.route("/youtube/accounts/applelogin2", methods=['POST'])
def legacy_login_bypass2():
    return f'''Auth={uuid4().hex}'''

# --------------------------------------------- #

@static.route("/youtube/accounts/registerDevice", methods=['POST'])
def login_bypass():
    # return random key
    key = uuid4().hex
    return f"DeviceId={key}\nDeviceKey={key}"

# --------------------------------------------- #