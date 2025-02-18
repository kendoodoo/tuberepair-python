# TubeRepair server, using Flask and Jinja2.
- __Works out of the box, edit the backend to your likings.__
- __Fetches from Youtube Private API without using a key (Coming soon!)__
- Works with Classic YouTube (iOS 5,6), 1.1.0 and 1.2.1 (Possibly 2.2.0 soon)
- ⚠️ This project is usable now, but still in beta. You can help me via @69kb (discord) ⚠️

### Current servers (Thanks for the hosting!):
- https://testtuberepair.uptimetrackers.com/
- host yourself. I don't deal with bullshit like "not working".

# Features
- Cache API responses
- Customizable config

### In the future
- Based all requests via innertube (ditching invidious and request to youtube Private API directly)
- Private server with password protection and secrets

# Setup
Make sure you have Python (3.8 minimum) and virtualenv (optional) installed.
```bash
# Download
git clone https://github.com/kendoodoo/tuberepair-python
cd tuberepair-python

# Preparing virtualenv
# You can just skip to pip, but for good measures.
virtualenv tuberepair
source tuberepair/bin/activate
pip install -r requirements.txt

# Running
python main.py
```
