from django.db.models.signals import post_save
from django.dispatch import receiver
from userauths.models import User
from account.models import Account  # Make sure to adjust this import based on your app structure

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    try:
        instance.account.save()
    except Account.DoesNotExist:
        pass