from django.db import models

# Create your models here.


class Notice_board(models.Model):
    title = models.CharField(max_length=150,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    
    
    
    
    
    
    def __str__(self):
        return self.title
