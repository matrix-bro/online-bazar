"""
ASGI config for online_bazar project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from environs import Env
env = Env()
env.read_env()

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_bazar.settings')

if env('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = env('DJANGO_SETTINGS_MODULE')

application = get_asgi_application()
