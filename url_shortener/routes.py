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
    url = request.form['url']
    if not url_validate(url):
        return jsonify({'error': 'incorrect url'})
    hours = request.form['hours']
    storage_time = timedelta(hours=int(hours))
    estimated_date = datetime.utcnow() + storage_time
    shortened = token_urlsafe(4)
    url_obj = URL(url=url, shortened=shortened, estimated_date=estimated_date)
    try:
        db.session.add(url_obj)
        db.session.commit()
    except:
        return jsonify({'error': 'internal server error'}), 500
    return jsonify({'shortened': shortened, 'estimated_date': estimated_date.strftime('%d.%m.%Y %H:%M:%S')})


@app.route('/<string:shortened>')
def return_redirect(shortened):
    url = URL.query.filter_by(shortened=shortened).first()
    print(url)
    if url:
        return redirect(url.url, code=302)
    else:
        flash('This link is invalid or expired!', 'danger')
    return redirect(url_for('home'))
