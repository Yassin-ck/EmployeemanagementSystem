from .models import User,Code
from django.db.models.signals import post_save
from django.dispatch import receiver
# from 

@receiver(post_save, sender=User)
def post_save_generator_code(sender,instance,created,*args,**kwargs):

    if created:
        Code.objects.create(user=instance)

# failed_login