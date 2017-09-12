"""
WSGI config for irkshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irkshop.settings")

application = Sentry(get_wsgi_application())
