from .models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import random

User = get_user_model()


@receiver(post_save, sender=Post)
def send_notification_email(sender, instance, created, **kwargs):
    if not created:
        return

    admins = list(User.objects.filter(is_staff=True, is_active=True, email__isnull=False))

    if not admins:
        return

    admin = random.choice(admins)

    subject = f'New post by {instance.author.username}'
    post_url = instance.get_absolute_url()
    message = f'A new post titled "{instance.title}" has been created. You can view it here: \nhttp://localhost:8000/{post_url}/'

    send_mail( subject,
               message,
               instance.author.email,
               [admin.email],
               fail_silently = False,
         )