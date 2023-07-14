# from accounts.models import User
# from .models import UserProfile
# from django.db.models.signals import post_save,pre_save
# from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def post_save_create_user_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
    
    # Handle updating the UserProfile when editing the User
    # try:
    #     profile = instance.userprofile
    # except UserProfile.DoesNotExist:
    #     profile = None
    
    # if profile:
    #     profile.profile_picture = instance.userprofile.profile_picture  # Assuming the UserProfile model has an 'image' field named 'profile_picture'
    #     profile.save()
