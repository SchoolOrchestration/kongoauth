# kongoauth
A collection of utilities for implementing Kong OAuth with Django Rest Framework


## Status

[![CircleCI](https://circleci.com/gh/SchoolOrchestration/kongoauth.svg?style=svg)](https://circleci.com/gh/SchoolOrchestration/kongoauth)
[![PyPI version](https://badge.fury.io/py/django-kongoauth.svg)](https://badge.fury.io/py/django-kongoauth)


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
docker-compose run --rm web python manage.py test
```

**Upload to pypi**
check if you have the correct permissions first then
install: 
- twine
```bash
# change the version in setup.py then run
python setup.py sdist

twine upload dist/twine upload dist/django-kongoauth-<version>.tar.gz 

```
