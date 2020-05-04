from __future__ import absolute_import, unicode_literals

import sendgrid
from celery.schedules import crontab
from celery.task import periodic_task
from sendgrid.helpers.mail import *

import settings
from apps.mailing.models import MailingHistory
from apps.myauth.models import User


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="send_daily_email",
    ignore_result=True
)
def send_daily_email():
    message = 'Hi, we have something new for you! Come and see us!'
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email(settings.EMAIL_HOST_USER)
    subject = 'ImageStock news'
    to_emails = User.objects.values_list('email', flat=True)
    content = Content('text/plain', message)
    mail = Mail(from_email, subject, to_emails, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    MailingHistory.objects.create(message=message, receivers=to_emails)
