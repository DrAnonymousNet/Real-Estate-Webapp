from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from realEstate.models import Agent

"""
@receiver(post_save, sender=User)
def create_agent(sender, instance, created, *args, **kwargs):
    if created:
        Agent.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_agent(sender, instance, *args, **kwargs):
    instance.agent.save()
"""