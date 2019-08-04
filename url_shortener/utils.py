import os
from datetime import datetime
from urllib.parse import urlparse

def url_validate(url):
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])
    except:
        return False