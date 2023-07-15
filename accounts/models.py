from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import secrets
from datetime import datetime
from django.utils  import timezone 
from django.contrib.auth.models import Group

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        HR = 'HR','Hr'
        MANAGER = 'MANAGER','Manager'
        WORKER = 'WORKER','Worker'
    class Department(models.TextChoices):
        FRONTEND = 'FRONTEND','Frontend'
        BACKEND = 'BACKEND','Backend'
        TESTING = 'TESTING','Testing'        
            
    base_role = Role.HR 
    
    username = models.CharField(max_length=150,null=True,unique=True,blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(default=None,max_length=13)
    role = models.CharField(max_length=50,choices=Role.choices)
    department = models.CharField(max_length=50,choices=Department.choices)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','department','mobile']
    
    
    
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.base_role
            super().save(*args, **kwargs)  # Save the user before adding to the group
            hr_group = Group.objects.get(name='HumanResource')
            self.groups.add(hr_group)
            print(';hhhhh')
        else:
            
            super().save(*args, **kwargs)  
        
        
        
class Code(models.Model):
    number = models.CharField(max_length=20,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    
    def __str__(self):
        return str(self.number)   
    

    def save(self,*args,**kwargs):
        otp = random.randint(100000, 999999)
        otp=''.join(secrets.choice(str(otp))for i in range(6))
        self.number = otp
        super().save(*args,**kwargs)
        
        
        





