from secrets import token_urlsafe
from datetime import datetime, timedelta
from flask import url_for, render_template, redirect, request, jsonify
from url_shortener import app, db
from url_shortener.models import URL

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['url']
    hours = request.form['store_time']
    storage_time = timedelta(hours=hours)
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
    redirect(url_for('home'))
