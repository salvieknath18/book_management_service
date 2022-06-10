import unittest
import json

from app import app
from models.db import db
from tests.test_data import *
from errors import UnauthorizedError


class UserTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.db = db.get_db()
        self.add_admin_user_for_testing()
        self.token = None
        self.get_token_for_testing()

    def add_admin_user_for_testing(self):
        collection = self.db['user']
        collection.insert_one(admin_user)

    def get_token_for_testing(self):
        payload = json.dumps({'email': 'admin@gmail.com', 'password': 'admin_123'})
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=payload)
        self.token = response.json['token']

    def test_login_success(self):
        # Given
        payload = json.dumps({'email': 'admin@gmail.com', 'password': 'admin_123'})

        # When
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)

    def test_login_failure(self):
        # Given
        payload = json.dumps({'email': 'myadmin@gmail.com', 'password': 'admin_123'})

        # When
        with self.assertRaises(UnauthorizedError):
            self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        # Should be handled through UnauthorizedError exception above

    def test_user_add(self):
        # Given
        payload = json.dumps(dummy_user)

        # When
        response = self.app.post('/api/auth/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_user_list(self):
        # Given
        # payload = json.dumps({'email': 'admin@gmail.com', 'password': 'admin_123'})

        # When
        response = self.app.get('/api/users', headers={"Content-Type": "application/json"})

        # Then
        self.assertEqual(list, type(response.json))
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
