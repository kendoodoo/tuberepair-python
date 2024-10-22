import werkzeug
from modules import get
from .logs import text

valid_search_orderby = {
    'relevance': 'relevance',
    'published': 'date',
    'viewCount': 'views',
    'rating': 'rating'
}

valid_search_time = {
    'today': 'today',
    'this_week': 'week',
    'this_month': 'month'
}

valid_search_duration = {
    'short': 'short',
    'long': 'long'
}

proxies = None

def setup_proxies(proxy):
    global proxies
    proxies = {
        "http": proxy,
        "https": proxy
    }

def process_start_index(request):
    if type(request) is not werkzeug.local.LocalProxy:
        raise ValueError("request SHOULD BE werkzeug.local.LocalProxy! SOMETHING IS WRONG!")
    
    # Getting current url with all the query info
    next_page = request.url
    # Get 'start-index' query for later use
    start_index = request.args.get('start-index')
    # Get current page or start at the first page if 'start-index' is missing or invalid
    if start_index and start_index.isdigit():
        current_page = start_index
    else:
        current_page = '1'
    # Setup for next page
    next_pageNumber = int(current_page) + 1
    # Checks if we have a 'start-index'
    if start_index:
        # Replace for next page
        next_page = next_page.replace(f'start-index={current_page}', f'start-index={next_pageNumber}')
    else:
        # Add query for next page
        next_page += f'&start-index={next_pageNumber}'
    # Santize
    next_page = next_page.replace('&', '&amp;')

    return current_page, next_page

def string_to_bool(input):
    if not isinstance(input, str):
        raise ValueError("A String was not passed")
    lower_input = input.lower()
    if lower_input == "true":
        return True
    elif lower_input == "false":
        return False
    raise ValueError("This string isn't true of false!")