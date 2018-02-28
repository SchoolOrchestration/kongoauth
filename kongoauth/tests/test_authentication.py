# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.contrib.auth import get_user_model

from ..authentication import KongOAuthAuthentication
from ..helpers import get_redis
from .testutils import get_user_data

import json

class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.auth = KongOAuthAuthentication()

    def test_autenticate(self):
        headers = {
            'HTTP_X_AUTHENTICATED-USERID': '1'
        }
        request = self.rf.get('/', **headers)
        user = self.auth.authenticate(request)

    def test_anon_authenticate(self):
        pass

class AuthenticationUserSerializationTestCase(TestCase):

    def setUp(self):
        redis = get_redis()
        self.user_id = 1
        user_permission_data = get_user_data(self.user_id)
        redis.set('authorization.1', user_permission_data)
        self.auth = KongOAuthAuthentication()

    def test_it_gets_user_from_redis(self):

        result = self.auth.get_user(self.user_id)



