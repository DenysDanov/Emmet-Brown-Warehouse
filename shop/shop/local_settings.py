import os
from django.core.management.commands.runserver import Command as runserver

ALLOWED_HOSTS = ['*']
runserver.default_port = os.environ.get('PORT') or 8000
# SMTP_USER = (os.environ.get('SMTP_USERNAME'),os.environ.get('SMTP_PASSWORD'))
SMTP_USER = (os.environ.get('SMTP_USERNAME'),os.environ.get('SMTP_PASSWORD'))
SMTP_APIKEY = os.environ.get('STMP_APIKEY')
SMTP_SERVER = (os.environ.get('SMTP_SERVER'),os.environ.get('SMTP_PORT'))
ADMIN_MAIL = 'denysdanov@gmail.com'