from django.db import models
from django.contrib.auth.models import AbstractUser
import sys

# Create your models here.

   
    
# class Role(models.Model):
#     names = models.CharField(max_length=20)
    
#     def __str__(self):
#         return self.names
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
    mobile = models.CharField(default=None,null=True,unique=True,max_length=10)
    role = models.CharField(max_length=50,choices=Role.choices)
    department = models.CharField(max_length=50,choices=Department.choices)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','department']
    def save(self,*args,**kwargs):
        if self.is_superuser:
            self.role = self.base_role
            # self.department =
            return super().save(*args,**kwargs)
            
        else:
            return super().save(*args,**kwargs)
        
    
   
        
     
    