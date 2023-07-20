from .models import User,Code
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from employee_dashboard.models import UserProfile
@receiver(post_save, sender=User)
def post_save_generator_code(sender,instance,created,*args,**kwargs):

    if created:
        if instance.is_superuser:
            Code.objects.create(user=instance)
            UserProfile.objects.create(user=instance)
        else:
            Code.objects.create(user=instance)
            
