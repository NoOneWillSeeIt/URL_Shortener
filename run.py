#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from url_shortener import create_app, db
from url_shortener.models import URL

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

if __name__ == '__main__':
    manager.run()