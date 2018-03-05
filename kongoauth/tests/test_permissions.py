from rest_framework.test import APIClient as Client
from .testutils import get_user_data
from django.test import TestCase
from ..helpers import get_redis
from example.api import Example


class KongOAuthPermissionTestCase(TestCase):

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
        response = self.client.get('/example/', **self.headers)
        self.assertTrue(response.status_code == 200,
                        msg='Valid Permissions Fail')

    def test_patch_request_has_no_permissions(self):
        response = self.client.patch(
            '/example/{}/'.format(self.example.id),
            **self.headers
        )
        self.assertTrue(response.status_code == 200,
                        msg='Valid Permissions Fail')

    def test_put_request_has_no_permissions(self):
        response = self.client.put(
            '/example/{}/'.format(self.example.id),
            data={
                'name': 'example'
            },
            **self.headers
        )
        self.assertTrue(response.status_code == 200,
                        msg='Valid Permissions Fail')

    def test_post_has_invalid_permissions(self):
        response = self.client.post(
            '/example/',
            data={
                'name': 'example'
            },
            **self.headers
        )
        self.assertTrue(response.status_code == 403,
                        msg='Invalid Permissions Passes')

    def test_delete_not_allowed(self):
        response = self.client.delete(
            '/example/{}/'.format(self.example.id),
            **self.headers
        )
        self.assertTrue(response.status_code == 403,
                        msg='Invalid Permissions Passes')
