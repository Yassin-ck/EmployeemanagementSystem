from django import forms
from .models import Notice_board,Department_notice,LeaveApply,TodayTasks,Paycheque
from PIL import Image
class DateInput(forms.DateInput):
    input_type='date'    

class NoticeboardForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    # def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     if image:
    #         img = Image.open(image)
    #         max_width =1000
    #         max_height =1000
    #         if img.width > max_width or img.height >max:
    #             raise forms.ValidationError('The image size exceeds the allowed limit')
    #     return image
    class Meta:
        model = Notice_board
        fields = ('title','subject','content','image')
        
        def __init__(self,*args,**kwargs):
            super().save(*args,**kwargs)
            self.fields['image'].required = False
        
        
class DepartmentnoticeForm(forms.ModelForm):
    title =  forms.CharField(required=False)
    subject =  forms.CharField(required=False)
    class Meta:
        model = Department_notice
        fields = ('title','subject','content','image')
        
        
# Dateinput        

class LeaveForm(forms.ModelForm):  
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    reason = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = LeaveApply
        fields = ('start_date','end_date','reason')
       
       


class TodayTaskForm(forms.ModelForm):
    
    class Meta:
        model = TodayTasks
        fields = ('comment',)
        
        

class PaychequeForm(forms.ModelForm): 
    pay_period = forms.DateField(widget=DateInput)
       
    class Meta:
        model = Paycheque
        fields = ('user','pay_period','gross_salary','deductions','net_pay','incentives_bonus')