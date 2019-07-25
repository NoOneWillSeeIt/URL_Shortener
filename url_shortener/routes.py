from datetime import datetime, timedelta
from flask import url_for, render_template, redirect, request, jsonify, flash
from secrets import token_urlsafe
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from url_shortener import app, db
from url_shortener.models import URL
from url_shortener.utils import log_error, url_validate

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/shrink', methods=['POST'])
def shrink():
    try:
        url = request.form['url']
        if not url_validate(url):
            return jsonify({'error': 'incorrect url'})
        hours = int(request.form['hours'])
    except:
        return jsonify({'error': 'incorrect request'}), 400

    if hours > app.config['MAX_STORAGE_TIME']:
        hours = app.config['MAX_STORAGE_TIME']

    estimated_date = datetime.utcnow() + timedelta(hours=hours)
    
    for rounds in range(0,5):
        shortened = token_urlsafe(4)
        url_obj = URL(url=url, shortened=shortened, estimated_date=estimated_date)
        try:
            db.session.add(url_obj)
            db.session.commit()
            break
        except IntegrityError as err:
            db.session.rollback()
        except SQLAlchemyError as err:
            db.session.rollback()
            log_error(err)
    else:
        return jsonify({'error': 'internal server error'}), 500

    return jsonify({'shortened': \
                    url_for('return_redirect', shortened=shortened, _external=True),
                    'estimated_date': \
                    estimated_date.strftime('%d.%m.%Y %H:%M:%S')})


@app.route('/l/<string:shortened>/')
def return_redirect(shortened):
    url = URL.query.filter_by(shortened=shortened).first()
    if url:
        if datetime.utcnow() < url.estimated_date:
            return redirect(url.url, code=302)
        else:
            try:
                db.session.delete(url)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                log_error(err)
                
    flash('This link is invalid or expired!', 'danger')
    return redirect(url_for('home'))
