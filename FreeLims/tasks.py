from celery import Celery
from django.core.mail import send_mail
from celery import shared_task

#celery = Celery('tasks', broker='amqp://guest@localhost//')

@shared_task
def registrationEmail(email_subject, email_body, email, html_message):
    send_mail(
        email_subject,
        email_body,
        'caretagus@gmail.com',
        [email],
        fail_silently=True,
        html_message=html_message
    )

@shared_task
def secretKeyResetEmail(email_subject, email_body, email, html_message):
    send_mail(
        email_subject,
        email_body,
        'caretagus@gmail.com',
        [email],
        fail_silently=True,
        html_message=html_message
    )
@shared_task
def reportProblemEmail(email_subject, email_body, email):
    send_mail(
        email_subject,
        email_body,
        email,
        ['caretagus@gmail.com'],
        fail_silently=True
    )

@shared_task
def landingPageContactEmail(contact_name, contact_email, contact_sub, contact_message):
    send_mail(
        'Message From: ' + contact_name + ' about ' + contact_sub,
        contact_message,
        contact_email,
        ['caretagus@gmail.com'],
        fail_silently=False,
    )