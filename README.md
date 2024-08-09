# Paused due to personal problems. Code's done, so don't worry.
# TubeRepair custom backend, using Flask and Jinja2.
- __A self-hosting solution to edit the backend to your likings.__
- __Fetches API from Invidious with no API authentication needed.__
- ⚠️ This project is still in beta. You can help or suggest ideas in [bag's discord](https://discord.bag-xml.com) ⚠️

# Features
- Cache API responses
- Customizable config

# Setup
Make sure you have Python 3 and virtualenv installed.
```bash
# Download
git clone https://github.com/kendoodoo/tuberepair-backend
cd tuberepair-backend
pip install -r requirements.txt

# Preparing virtualenv
virtualenv tuberepair # you can use any name, but for convenience
cd tuberepair
source bin/activate
cd ..

# Running
python main.py
```
Remember to edit config.py, otherwise it will not run properly

# Contributors

- [ObscureMosquito](https://github.com/ObscureMosquito)
- [SpaceSaver](https://github.com/SpaceSaver)
- (and me.)
