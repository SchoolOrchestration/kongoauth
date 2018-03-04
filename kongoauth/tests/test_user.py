# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .testutils import get_user_data

from ..user import TransientUser

import json


class UserTestCase(TestCase):

    def setUp(self):
        self.user_id = 1
        data = json.loads(get_user_data(self.user_id))
        self.user = TransientUser.from_redis_data(data)

    def test_it_sets_user_id(self):
        assert self.user.id == self.user_id

    def test_it_sets_groups(self):
        assert len(self.user.groups) == 1

    def test_it_sets_user_permissions(self):
        assert len(self.user.user_permissions) == 4

    def test_it_can_get_permissions_by_group(self):
        pass

    def test_it_can_verify_user_has_permission(self):
        assert self.user.has_perm('all') == True,\
            'Expected the user to have the all permission'

    def test_it_can_verify_user_does_not_have_permission(self):
        assert self.user.has_perm('illegal-permission') == False,\
            'Expected the user not to have the foo permission'

    def test_has_permissions(self):

        tests = [
            # input, expected result
            (['foo','bar','baz'], True), # user has more permissions than list provided
            (['not a permission','bar','baz'], False), # user has some permission, but is missing some
        ]
        for test_input, expected_result in tests:
            assert self.user.has_perms(test_input) == expected_result,\
                'Expected: {} to be: {}'.format(test_input, expected_result)
