from django.http import HttpResponseForbidden
from django.conf import settings
from rest_framework import permissions
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from .models import Product


def send_mail(user,password,target,header,content):
    try:
        print(settings.SMTP_SERVER[1])
        print(settings.SMTP_SERVER[1].replace('"', ''))
        print(type(settings.SMTP_SERVER[1]))
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = user
        message['To'] = target
        message['Subject'] = header

        #The body and the attachments for the mail
        message.attach(MIMEText(content, 'plain'))

        #Create SMTP session for sending the mail
        session = smtplib.SMTP(settings.SMTP_SERVER[0].replace('"', ''),int(settings.SMTP_SERVER[1].replace('"', ''))) #use mail with port
        session.starttls() #enable security
        session.login(user, password) #login with mail_id and password
        
        text = message.as_string()
        session.sendmail(user, target, text)
        session.quit()
    except Exception as e:
        print(f'Error [{e}] in main.service.send_mail occured')


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


def allowed_methods(*args):
    def wrapper(func):
        def wrapped(request):
            if request.method not in args: return HttpResponseForbidden('403 Forbidden')
            return func(request)
 
        return wrapped
 
    return wrapper