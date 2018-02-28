# kongoauth
A collection of utilities for implementing Kong OAuth with Django Rest Framework

## Setting it up in your project:

**Install:**

```
pip install ...
```

**Add to settings**

```
INSTALLED_APPS = [
    ..
    'kongoauth',
]
```

**Add DRF authentication class**

```
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'kongoauth.authentication.KongOAuthAuthentication',
    ),
    ...
}
```

**Optional settings**

* `AUTH_REDIS_KEY`
* `REDIS_CONN` # a dictionary with redis configs

## Run the tests

```
docker-compose run --rm web python example/manage.py test
```

