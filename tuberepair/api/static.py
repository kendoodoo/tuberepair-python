from flask import Blueprint, request, redirect, send_file, render_template, Response
import config
from uuid import uuid4

static = Blueprint("static", __name__, static_folder="../static")
# Still passed without unique keys.
key = uuid4().hex

# static contents
# --------------------------------------------- #

@static.route("/")
def index(res=None):
    return render_template('web/index.html', version=config.VERSION, medium=config.MEDIUM_QUALITY, hls=config.HLS_RESOLUTION)

# sidebar menu
@static.route("/schemas/2007/categories.cat")
@static.route("/<int:res>/schemas/2007/categories.cat")
def sidebar(res=None):
    return static.send_static_file('categories.cat')

# bypass login
# for youtube classic
@static.route("/youtube/accounts/applelogin1", methods=['POST'])
@static.route("/<int:res>/youtube/accounts/applelogin1", methods=['POST'])
def legacy_login_bypass(res=None):
    return f'''r2={key}\nhmackr2={key}'''

# second layer
# for youtube classic
@static.route("/youtube/accounts/applelogin2", methods=['POST'])
@static.route("/<int:res>/youtube/accounts/applelogin2", methods=['POST'])
def legacy_login_bypass2(res=None):
    return f'''Auth={key}'''

# --------------------------------------------- #
# bypass login for Google YT
@static.route("/youtube/accounts/registerDevice", methods=['POST'])
@static.route("/<int:res>/youtube/accounts/registerDevice", methods=['POST'])
def login_bypass(res=None):
    # return random key
    return f"DeviceId={key}\nDeviceKey={key}"

# --------------------------------------------- #
# feat: LOGIN. REAL FUCKING LOGIN.
# note: PLEASE, PLEASE figure out.

@static.route("/accounts/ClientLogin", methods=['POST'])
def login_rel():
    return '''SID=DQAAAGgA...7Zg8CTN\nLSID=DQAAAGsA...lk8BBbG\nAuth=DQAAAGgA...dk3fA5N'''