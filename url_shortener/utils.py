import os
from datetime import datetime
from urllib.parse import urlparse

def url_validate(url):
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])
    except:
        return False

def log_error(err):
    date = datetime.now()
    log_file = date.strftime('%d.%m.%Y') + '.txt'
    time = date.strftime('%H:%M:%S')
    if not os.path.exists('/logs'):
        os.makedirs('/logs')
    with open('/logs/'+log_file, 'a') as file:
        file.write(time + ': ' + err)
        file.write(err.args)