# beta 1.5 out now.
# TubeRepair server, using Flask and Jinja2.
- __Works out of the box, edit the backend to your likings.__
- __Fetches from Youtube Private API without using a key (Coming soon!)__
- Works with Classic YouTube, 1.1.0 and 1.2.1 (Possibly 2.2.0 soon)
- ⚠️ This project is usable now, but still in beta. You can help in [bag's discord](https://discord.bag-xml.com) ⚠️

### Current servers (Thanks for the hosting!):
- https://tuberepair.nugg3t.xyz/
- https://tuberepair.uptimetrackers.com/

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

# Credits

### Contributors
- [kendoodoo](https://github.com/kendoodoo) (God)
- [Nishijima Akito](https://github.com/shijimasoft) (Youtube Classic)
- [SpaceSaver](https://github.com/SpaceSaver) (YouTube Private API, HLS playback filter)
- (et al.)

### Code
I will not copy code that explicitly states "do not modify".
- https://github.com/ftde0/yt2009
__without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software__
- https://github.com/tombulled/innertube
__You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications__
