from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from django.conf import settings
from .user import TransientUser
from .helpers import get_redis
import json


class KongOAuthAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        Uses Kong's OAuth headers to create a a 'Transit' User
        note: this may need to be X_ (not HTTP_X_..) in real life:
        """
        anonymous = request.META.get("HTTP_X_ANONYMOUS_CONSUMER", None)
        if not anonymous:
            user_id = request.META.get("HTTP_X_AUTHENTICATED_USERID", None)
            user = self.get_user(user_id)
            return user, None
        else:
            return AnonymousUser(), False

    @staticmethod
    def get_user(user_id):
        """
        Gets User information from a permission redis instance
        """
        redis_key = getattr(settings, 'AUTH_REDIS_KEY',
                            'authorization.{}').format(user_id)
        redis = get_redis()
        user_data = redis.get(redis_key)
        user_data = json.loads(user_data)
        return TransientUser.from_redis_data(user_data)


class KongKeyAuthAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        pass
