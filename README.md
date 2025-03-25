# TubeRepair server, using Flask and Jinja2.
- __Works out of the box, edit the backend to your likings.__
- __Fetches from Youtube Private API without using a key__
- Works with Classic YouTube, 1.0 to 2.2.0 for Google YouTube
- ⚠️ This project is usable now, but still in beta. You can help in [bag's discord](https://discord.bag-xml.com) ⚠️
- ⚠️ You can also fork this repo and create pull request if you'll like to add or fix things!⚠️
  
# Features
- Cache API responses
- Customizable config
- Docker compatible
- Infinite scroling in search, channels, playlist, playlist videos, and comment
- Allows users to select a video resolution in URL (example.com/360)
- Supports sending request via proxie with Socks5 or Https (https://scrapfly.io/blog/python-requests-proxy-intro/)

### In the future
- Based all requests via innertube (ditching invidious and request to youtube Private API directly)
- Private server with password protection and secrets

# Setting up
Make sure you have Python (3.8 minimum) and virtualenv (optional) installed.
```bash
# Download
git clone https://github.com/kevinf100/tuberepair.uptimetrackers.com
mv tuberepair.uptimetrackers.com/ tuberepairdocker/
cd tuberepairdocker/tuberepair

# Preparing virtualenv
# You can just skip to pip, but for good measures.
virtualenv tuberepair
source tuberepair/bin/activate
pip install -r requirements.txt

# Running
python main.py
```

# Docker

Make sure you have Linux, ports 80 and 443 open, [Docker](https://docs.docker.com/engine/install/), and DNS record already pointing to your server.

```bash
# Download
git clone https://github.com/kevinf100/tuberepair.uptimetrackers.com
mv tuberepair.uptimetrackers.com/ tuberepairdocker/
cd tuberepairdocker
cp ./example/.env ../
cp ./example/docker-compose-example.yml ./example/docker-compose.yml 
```
### docker-compose setup
Next you'll need to edit the .env file or you can edit the docker-compose.yml directly.  
The .env in example is the bare minimum you need for the server to run.  
You can always add more to it.

<details>
<summary>If you're NOT running Docker rootless</summary>
<br>
Uncomment the lines in docker-compose.yml that say to uncomment it (Lines 38 and 56) and comment that lines above them (Lines 37 and 55).
Comment the user USERID line (line 3) in .env.
<br>
</details>

<details>
<summary>If you're running Docker rootless</summary>
<br>
Get your userid
<br><br>

```
bash
id -u
```
add it to USERID in the .env file.
<br>
</details>

### Start
Once you edit the docker-compose.yml you are done and can run the server!
```bash
# Start
docker compose up -d --build
```

# Credits

### Contributors
- [kendoodoo](https://github.com/kendoodoo) (God)
- [Nishijima Akito](https://github.com/shijimasoft) (Youtube Classic)
- [SpaceSaver](https://github.com/SpaceSaver) (YouTube Private API, HLS playback filter)
- [Kevinf100](https://github.com/kevinf100) (Added features from the fork)
- (et al.)

### Code
I will not copy code that explicitly states "do not modify".
- https://github.com/ftde0/yt2009
__without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software__
- https://github.com/tombulled/innertube
__You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications__
