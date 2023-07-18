from django.db import models
from accounts.models import User
from PIL import Image
from datetime import datetime
from django.shortcuts import HttpResponse
from django.core.files.storage import default_storage
from django.utils.timezone import now
# Create your models here.
class Notice_board(models.Model):
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/',blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-updated_at','-created_at']
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.image:
            img = Image.open(self.image.path)
            
            if img.height > 85 or img.width > 85:
                output_size = (85,85)
                img.thumbnail(output_size)
                img.save(self.image.path)
        else:
            super().save(*args, **kwargs)

    
    
    
    def __str__(self):
        return self.title


class Department_notice(models.Model):
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='department/',blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-updated_at','-created_at']
        
        
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.image:
            img = Image.open(self.image.path)
            
            if img.height > 85 or img.width > 85:
                output_size = (85,85)
                img.thumbnail(output_size)
                img.save(self.image.path)
        else:
            super().save(*args, **kwargs)         


            
            
class LeaveApply(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()  
    approved_by_hr =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='approved_leaves_hr',blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank =True,default='Pending') 

 

    class Meta:
        ordering = ['-updated_at','-created_at']
        
        
        
    def __str__(self) :
        return f"{self.user.username}'s Leave Request"
    
    
   


class TodayTasks(models.Model):
    department_notice_board = models.ForeignKey(Department_notice, on_delete=models.CASCADE, null=True,related_name='department_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    comment = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated_at','-created_at']
    
    
    
    def __str__(self):
        if self.department_notice_board:
            return f'{self.user} commented on DepartmentBoard : {self.comment}'
        else:
            return f'{self.user} commented on NoticeBoard : {self.comment}'



class Paycheque(models.Model):
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='paychequed_by',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='paycheques',
    )
    base_salary = models.DecimalField(max_digits=15, decimal_places=4)
    allowances = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    overtime_pay_rate = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    bonus = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    deductions = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    salary = models.DecimalField(max_digits=15, decimal_places=4,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def Total_salary(self):
        salary = self.base_salary+self.allowances
        overtime_salary = self.overtime_hours * self.overtime_pay_rate
        salary +=overtime_salary
        salary +=self.bonus
        salary -=self.deductions
        return salary
    
    
    class Meta:
        ordering = ['-updated_at','-created_at']

   
    def __str__(self):
        return f'{self.employer} paid {self.salary} as salary to {self.user}'
        





class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    income = models.FloatField(null=True)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=20, unique=False)
    state = models.CharField(max_length=20, unique=False)
    country = models.CharField(max_length=20, unique=False)
    alternative_contact_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to="userprofile/")
    experience = models.CharField(max_length=255)
    
    
    
    
    
    # def __str__(self):
    #     return self.user.username 
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            
            if img.height > 85 or img.width > 85:
                output_size = (85,85)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
             
    
    # def save(self, *args, **kwargs):
    #     if self.pk and self.profile_picture:
    #         old_obj = UserProfile.objects.get(pk=self.pk)
    #         if self.profile_picture != old_obj.profile_picture:
    #             # Delete the old profile picture
    #             old_profile_picture = old_obj.profile_picture
    #             if default_storage.exists(old_profile_picture.name):
    #                 default_storage.delete(old_profile_picture.name)

    #     super().save(*args, **kwargs)
    
    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #     if self.profile_picture:
    #         img = Image.open(self.profile_picture.path)
            
    #         if img.height > 85 or img.width > 85:
    #             output_size = (85,85)
    #             img.thumbnail(output_size)
    #             img.save(self.profile_picture.path)
    #     else:
    #         self.profile_picture.save()
                
   
            
