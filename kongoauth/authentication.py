from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from .helpers import get_redis
from .user import TransientUser

import json

class KongOAuthAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        ## note: this may need to be X_ (not HTTP_X_..) in real life:
        anonymous = request.META.get('HTTP_X_ANONYMOUS_CONSUMER', None)
        if not anonymous:
            user_id = request.META.get('HTTP_X_AUTHENTICATED-USERID', None)
            user = self.get_user(user_id)
            return user, None
        else:
            return AnonymousUser(), False

    def get_user(self, user_id):
        '''
        '''
        redis_key = getattr(settings, 'AUTH_REDIS_KEY', 'authorization.{}').format(user_id)
        redis = get_redis()
        user_data = json.loads(redis.get(redis_key))

        return TransientUser.from_redis_data(user_data)

