# Handle innertube's format (in general)
from datetime import timedelta, datetime

# convert subscriber to text
# example: 10.1M (as string) -> 10100000 (as int)
def subscribers(string):
    processed_string = string.replace('subscribers', '')

    if 'M' in processed_string:
        return int(float(processed_string.replace('M', '')) * 100000.0)

    if 'K' in processed_string:
        return int(float(processed_string.replace('K', '')) * 1000.0)
    
    else:
        return processed_string

# convert views to text
# example: '123,498 views' (as string) -> 123498 (as int)
def views(string):
    processed_string = str(string).replace(' views', '').replace(',', '')
    return int(processed_string)

# convert yt timestamp to seconds (thanks stackoverflow)
# example 40:56 -> in seconds (as int)
def to_seconds(timestr):
    seconds = 0
    for part in timestr.split(':'):
        seconds = seconds * 60 + int(part, 10)
    return seconds

# convert annoying time string
# TODO: do we need to get the exact timezone?
# '1 hours ago' -> unix
def date_converter(string):

    # ['1', 'hours', 'ago']
    split_string = string.split(' ')
    current_time = datetime.now()

    # I have to do this manually because python librarys are not perfect.
    if split_string[1] == "minutes":
        return current_time - timedelta(minutes=int(split_string[0]))
    if split_string[1] == "hours":
        return current_time - timedelta(hours=int(split_string[0]))
    if split_string[1] == "days":
        return current_time - timedelta(days=int(split_string[0]))
    if split_string[1] == "months":
        return current_time - timedelta(weeks=int(split_string[0] * 4))
    if split_string[1] == "years":
        return current_time - timedelta(days=int(split_string[0]) * 365)

class misc:

    # Thanks to spacesaver.
    def hls_quality_split(hls, res=None):
        panda = hls.split("\n")
        # regex filter
        formatfilter = re.compile(r"^#EXT-X-STREAM-INF:BANDWIDTH=(?P<bandwidth>\d+),CODECS=\"(?P<codecs>[^\"]+)\",RESOLUTION=(?P<width>\d+)x(?P<height>\d+),FRAME-RATE=(?P<fps>\d+),VIDEO-RANGE=(?P<videoRange>[^,]+),AUDIO=\"(?P<audioGroup>[^\"]+)\"(,SUBTITLES=\"(?P<subGroup>[^\"]+)\")?")
        vertical = None
        maxRes = 0
        wanted_resolution = res and type(res) == int and min(max(res, 144), config.RESMAX) or config.HLS_RESOLUTION or 360
        # doesn't bother to explain the code, sooo...
        # TODO: explain the thing, lazer eyed cat.
        for x in range(len(panda)):
            line = panda[x]
            match = formatfilter.match(line)

            # dude
            if not match:
                continue
            
            # continue if codecs is not compatible (or matched?)
            if not match.group("codecs").startswith("avc"):
                panda[x] = ""
                panda[x+1] = ""
                continue
            
            # reject framerates over 30
            if int(match.group("fps")) > 30:
                panda[x] = ""
                panda[x+1] = ""
                continue
            
            if vertical is None:
                vertical = int(match.group("height")) > int(match.group("width"))
            res = 0

            # match vertical with width, because higher
            if vertical:
                res = int(match.group("width"))
            else:
                res = int(match.group("height"))

            # if resolution bigger than the expected height, skip
            if res > wanted_resolution:
                panda[x] = ""
                panda[x+1] = ""
                continue

            if res > maxRes:
               maxRes = res

        for x in range(len(panda)):
            line = panda[x]
            match = formatfilter.match(line)

            if not match:
                continue
            res = 0

            if vertical:
                res = int(match.group("width"))
            else:
                res = int(match.group("height"))

            if res < maxRes:
                panda[x] = ""
                panda[x+1] = ""

        panda = "\n".join(panda)
        return panda