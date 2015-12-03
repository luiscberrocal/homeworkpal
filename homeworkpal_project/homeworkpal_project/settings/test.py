from __future__ import absolute_import

from .base import *
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['example.com', '127.0.0.1']
########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
