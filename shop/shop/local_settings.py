import os
from django.core.management.commands.runserver import Command as runserver

ALLOWED_HOSTS = ['*']
runserver.default_port = os.environ.get('PORT') or 8000