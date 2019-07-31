import os
import json
import unittest
from flask import current_app, url_for
from url_shortener import create_app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_shrinking_func(self):
        response = self.client.post(url_for('routes.shrink'), data={
            'url': 'www.google.com'
            })
        response_body = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 400)
        self.assertTrue(response_body['error'] == 'incorrect url')

        response = self.client.post(url_for('routes.shrink'), data={
            'url': 'https://www.google.com/'
            })
        response_body = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 400)
        self.assertTrue(response_body['error'] == 'incorrect request')

        response = self.client.post(url_for('routes.shrink'), data={
            'url': 'https://www.google.com/',
            'hours': 24
            })
        response_body = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response_body['shortened'])

    def test_redirect_func(self):
        response = self.client.post(url_for('routes.shrink'), data={
            'url': 'https://www.google.com/',
            'hours': 24
            })
        response_body = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response_body['shortened'])

        response = self.client.get(response_body['shortened'], follow_redirects=False)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.location == 'https://www.google.com/')
