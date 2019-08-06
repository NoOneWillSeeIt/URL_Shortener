import os
from datetime import datetime
from urllib.parse import urlparse
from url_shortener import db
from url_shortener.models import URL

def url_validate(url):
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])
    except:
        return False

def delete_overdue_urls():
    url_list = URL.query.filter_by(datetime.utcnow() > estimated_date).all()
    try:
        for url in url_list:
            db.session.delete(url)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()