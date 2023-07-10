from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import secrets

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
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','department','mobile']
    def save(self,*args,**kwargs):
        if self.is_superuser:
            self.role = self.base_role
            # self.department =
            return super().save(*args,**kwargs)
            
        else:
            return super().save(*args,**kwargs)
          
        
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
        
        
        
    