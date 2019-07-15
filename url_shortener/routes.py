from secrets import token_urlsafe
from datetime import datetime, timedelta
from urllib.parse import urlparse
from flask import url_for, render_template, redirect, request, jsonify, flash
from url_shortener import app, db
from url_shortener.models import URL

@app.route('/')
def home():
    return render_template('main.html')

def url_validate(url):
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])
    except:
        return False

@app.route('/process', methods=['POST'])
def process():
    url = ''
    hours = 0
    try:
        url = request.form['url']
        if not url_validate(url):
            return jsonify({'error': 'incorrect url'})
        hours = request.form['hours']
    except:
        return jsonify({'error': 'incorrect request'}), 500

    storage_time = timedelta(hours=int(hours))
    estimated_date = datetime.utcnow() + storage_time
    
    shortened = ''
    tries = 0
    while(True):
        try:
            shortened = token_urlsafe(4)
            url_obj = URL(url=url, shortened=shortened, estimated_date=estimated_date)
            db.session.add(url_obj)
            db.session.commit()
            break
        except:
            tries += 1
            if tries > 4:
                return jsonify({'error': 'internal server error'}), 500

    return jsonify({'shortened': shortened, 'estimated_date': estimated_date.strftime('%d.%m.%Y %H:%M:%S')})


@app.route('/<string:shortened>')
def return_redirect(shortened):
    url = URL.query.filter_by(shortened=shortened).first()
    if url:
        if datetime.utcnow() < url.estimated_date:
            return redirect(url.url, code=302)
        else:
            db.session.delete(url)
            db.session.commit()
    flash('This link is invalid or expired!', 'danger')
    return redirect(url_for('home'))
