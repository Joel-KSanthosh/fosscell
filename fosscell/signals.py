# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from .models import User, Institution

@receiver(post_save, sender=User)
def create_institution(sender, instance, created, **kwargs):
    if created:
        institution_name = instance.institution

        # Check if the institution already exists
        Institution = apps.get_model('fosscell', 'Institution')
        institution, created = Institution.objects.get_or_create(name=institution_name)

        if created:
            print(f"New institution created: {institution_name}")
        else:
            print(f"Institution already exists: {institution_name}")
