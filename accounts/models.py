from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Department(models.Model):
    name =models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
# class Role(models.Model):
#     names = models.CharField(max_length=20)
    
#     def __str__(self):
#         return self.names
    
class User(AbstractUser):
    class Role(models.TextChoices):
        HR = 'HR','hr'
        MANAGER = 'MANAGER','manager'
        WORKER = 'WORKER','worker'
            
    base_role =Role.HR   
    username = models.CharField(max_length=150,null=True,unique=True,blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(default=None,null=True,unique=True,max_length=10)
    role = models.CharField(max_length=50,choices=Role.choices)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def save(self,*args,**kwargs):
        if self.is_superuser or self.department.name =='Hr':
            # self.department = 'HR'
            self.role = self.base_role
            return super().save(*args,**kwargs)
        else:
            return super().save(*args,**kwargs)
   
        
     
    