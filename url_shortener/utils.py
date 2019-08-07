import os
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
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
    try:
        URL.query.filter(datetime.utcnow() > URL.estimated_date).delete()
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()