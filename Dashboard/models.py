from django.db import models
from accounts.models import User
from PIL import Image

# Create your models here.


class Notice_board(models.Model):
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/',blank=True)

    
    
    
    
    
    
    def __str__(self):
        return self.title


class Department_notice(models.Model):
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='department/',blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 85 or img.width > 85:
            output_size = (85,85)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
            
class LeaveApply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()  
    approved_by_hr =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='approved_leaves_hr',blank=True)
    
    def __str__(self) :
        return f"{self.user.username}'s Leave Request"
    
    
   
