#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import redis
from datetime import datetime, timedelta
from flask import request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from rq_scheduler import Scheduler
from url_shortener import babel, create_app, db
from url_shortener.models import URL
from url_shortener.utils import delete_overdue_urls

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, URL=URL)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('url_shortener.tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    from flask_migrate import upgrade
    upgrade()
    db.create_all()


try:
    redis_url = app.config['REDISTOGO_URL']
    conn = redis.from_url(redis_url)
    conn.ping()
except redis.ConnectionError as err:
    pass
else:
    scheduler = Scheduler(connection=conn)
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=delete_overdue_urls,
        args=None,
        kwargs=None,
        interval=timedelta(hours=48).total_seconds(),
        repeat=None,
        meta=None
    )


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    manager.run()