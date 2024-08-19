# v0.0.2 is out! Try it.
# TubeRepair custom backend, using Flask and Jinja2.
- __A self-hosting solution to edit the backend to your likings.__
- __Fetches API from Invidious with no API authentication needed.__
- Works from 1.0.0 to 1.2.1
- ⚠️ This project is usable now, but still in beta. You can help in [bag's discord](https://discord.bag-xml.com) ⚠️

A server is live right now, thanks to nugg3t! https://tuberepair.nugg3t.xyz/

# Features
- Cache API responses
- Customizable config

### In the future
- Based all requests via innertube (ditching invidious and request to youtube Private API directly)

# Setup
Make sure you have Python 3 and virtualenv (optional) installed.
```bash
# Download
git clone https://github.com/kendoodoo/tuberepair-backend
cd tuberepair-backend

# Preparing virtualenv
# You can just skip to pip, but for good measures.
virtualenv tuberepair
source tuberepair/bin/activate
pip install -r requirements.txt

# Running
python main.py
```

# Contributors

- [kendoodoo](https://github.com/kendoodoo)
- [SpaceSaver](https://github.com/SpaceSaver) (A bunch of ideas, HLS playback filter)
- (et al.)
