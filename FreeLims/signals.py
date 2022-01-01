
import models
from models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
def notify_after_registration(sender, instance, created, **kwargs):
    user = instance
    email_subject = 'Account confirmation'
    email_body = "some message"
    send_mail(
        email_subject,
        email_body,
        instance.email,
        [instance.email],
        fail_silently=False
    )
post_save.connect(notify_after_registration, sender=User)
