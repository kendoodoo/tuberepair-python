# TubeRepair server, using Flask and Jinja2.
- __Works out of the box, edit the backend to your likings.__
- __Fetches from Youtube Private API without using a key__
- Works with Classic YouTube, 1.0 to 2.2.0 for Google YouTube
- ⚠️ This project is usable now, but still in beta. You can help in [bag's discord](https://discord.bag-xml.com) ⚠️
- ⚠️ You can also fork this repo and create pull request if you'll like to add or fix things!⚠️

### Current servers (Thanks for the hosting!):
#### This repo
Main stable server
- https://tuberepair.uptimetrackers.com/

Testing server
- https://testtuberepair.uptimetrackers.com/

#### Other people
- None! :(

# Features
- Cache API responses
- Customizable config
- Docker compatible
- Suggested in videos
- Search parameters sent by client are respected
- Infinite scroling in search, channels, playlist, playlist videos, and comment
- Allows users to select a video resolution with example.com/360
- Doesn't require slash at the end of url (Note, this might be because of nginx)
- Will get users real ip if using cloudflare
- Supports sending request via proxie with Socks5 or Https (https://scrapfly.io/blog/python-requests-proxy-intro/)
- Automatic ssl certs

### In the future
- Based all requests via innertube (ditching invidious and request to youtube Private API directly)
- Private server with password protection and secrets

# Docker Public Server Setup

### Git
Make sure you have Linux, ports 80 and 443 open, [docker](https://docs.docker.com/engine/install/), and DNS record already pointing to your server.
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
#### If your NOT running docker rootless
Uncomment the lines in docker-compose.yml that say to uncomment it (Lines 38 and 56) and comment that lines above them (Lines 37 and 55).
Comment the user USERID line (line 3) in .env.
 #### If your ARE running docker rootless
Get your userid
```bash
id -u
```
add it to USERID in the .env file.
 

### Start
Once you edit the docker-compose.yml you are done and can run the server!
```bash
# Start
docker compose up -d --build
```

# Docker Local/Private Setup
## Note this is not meant to be exposed to the internet in this config

### Git
Make sure you have Linux and [docker](https://docs.docker.com/engine/install/).
```bash
# Download
git clone https://github.com/kevinf100/tuberepair.uptimetrackers.com
mv tuberepair.uptimetrackers.com/ tuberepairdocker/
cd tuberepairdocker
cp ./example/.env ../
cp ./example/docker-compose-home-example.yml ./example/docker-compose.yml 
```
### docker-compose setup
Next you'll need to edit the .env file or you can edit the docker-compose.yml directly.  
#### If your NOT running docker rootless
Skip to start!
 #### If your ARE running docker rootless
You need to allow docker to expose a privileged port.  
https://docs.docker.com/engine/security/rootless/#exposing-privileged-ports  
__or__
change the port 80 on line 15 in docker-compose.yml to a port higher than 1023. I recommend 4000
 
### Start
Once you edit the docker-compose.yml you are done and can run the server!  
```bash
# Start
docker compose up -d --build
```

### Connecting to the server
#### If you didn't change the port in docker-compose.yml
You should be able to connect to it from your private ip.  
Example
```
http://192.168.0.100/
```
If that doesn't work try adding the port like this.
```
http://192.168.0.100:80/
```

#### If you changed the port in docker-compose.yml
You will need to add the port.
```
http://192.168.0.100:YOUR PORT YOU SET HERE/
```

# Old Setup that works without docker
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

# Credits

### Contributors
- [kendoodoo](https://github.com/kendoodoo) (God)
- [Nishijima Akito](https://github.com/shijimasoft) (Youtube Classic)
- [SpaceSaver](https://github.com/SpaceSaver) (YouTube Private API, HLS playback filter)
- [Kevinf100](https://github.com/kevinf100) (Added many features and created the docker container in this fork.)
- (et al.)

### Code
I will not copy code that explicitly states "do not modify".
- https://github.com/ftde0/yt2009
__without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software__
- https://github.com/tombulled/innertube
__You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications__
