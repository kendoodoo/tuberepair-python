from datetime import datetime

def unix(unix):
    return datetime.utcfromtimestamp(int(unix)).isoformat() + '.000Z'