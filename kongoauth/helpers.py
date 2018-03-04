from django.conf import settings
import redis


def get_redis():
    """
    Get a redis connection
    # rediss://:password@hostname:port/0
    """
    defualt_connection = {
        "host": "redis"
    }
    defualt_connection.update(getattr(settings, 'REDIS_CONN', {}))
    # return redis.Redis(**{"host": "redis"})
    return redis.Redis(**defualt_connection)
