from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3apeoe(rfqxy9ik1j_zlf4%dx7$hopd2x$bd@y$4j=+yhn9j8v'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'

try:
    from .local import *
except ImportError:
    pass
