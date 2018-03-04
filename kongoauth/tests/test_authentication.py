# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from ..authentication import KongOAuthAuthentication
from ..helpers import get_redis
from ..user import TransientUser

from .testutils import get_user_data

import json

class AuthenticationSuccessTestCase(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.auth = KongOAuthAuthentication()
        self.user_id = 1

        headers = {
            'HTTP_X_AUTHENTICATED_USERID': self.user_id
        }
        request = self.rf.get('/', **headers)
        self.user, self.result = self.auth.authenticate(request)

    def test_successfully_logs_in(self):
        assert self.result is None

    def test_autenticates_user(self):
        assert self.user.id == self.user_id

    def test_returns_transient_user(self):
        assert isinstance(self.user, TransientUser)


class AuthenticationFailureTestCase(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.auth = KongOAuthAuthentication()
        self.user_id = 1

        headers = {
            'HTTP_X_ANONYMOUS_CONSUMER': 'anon'
        }
        request = self.rf.get('/', **headers)
        self.user, self.result = self.auth.authenticate(request)

    def test_it_returns_an_anon_user(self):
        assert isinstance(self.user, AnonymousUser)

    def test_it_returns_logged_in_false(self):
        assert self.result == False


class AuthenticationUserSerializationTestCase(TestCase):

    def setUp(self):
        redis = get_redis()
        self.user_id = 1
        user_permission_data = get_user_data(self.user_id)
        redis.set('authorization.1', user_permission_data)
        self.auth = KongOAuthAuthentication()

    def test_it_gets_user_from_redis(self):
        result = self.auth.get_user(self.user_id)



