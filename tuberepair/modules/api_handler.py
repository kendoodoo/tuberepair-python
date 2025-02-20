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