from rest_framework.test import APIClient as Client
from .testutils import get_user_data
from django.test import TestCase
from ..helpers import get_redis
from example.api import Example


class KongOAuthFBVPermissionTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        redis = get_redis()
        self.user_id = 1
        self.example = Example.objects.create(name='example')
        user_permission_data = get_user_data(self.user_id)
        redis.set('authorization.1', user_permission_data)
        self.headers = {
            'HTTP_X_AUTHENTICATED_USERID': self.user_id
        }

    def test_get_request_has_permissions(self):
        response = self.client.get('/fbv/', **self.headers)
        self.assertTrue(response.status_code == 403,
                        msg='Valid Permissions Fail')
