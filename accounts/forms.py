from django import forms
from django.forms import PasswordInput
from .models import User,Code
import re

class UserForm(forms.ModelForm):
    mobile = forms.CharField(max_length=13)
    is_superuser = forms.CheckboxInput()
    is_staff = forms.CheckboxInput()
    is_worker = forms.CheckboxInput()

    class Meta:
        model = User
        exclude = ['password']
        
        fields = ('first_name','last_name','email','role','department','mobile','username')
                  
        error_messages = {
            'username':{
                'unique':'User with this EmployeeCode already exists'
            },
            'mobile':{
                'unique':'User with this  Mobile Number  already exists.'
            },
        }
        labels = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'email':'Email',
            'role':'Role',
            'department':'Department',
            'mobile':'Mobile Number',
            'username':'Employee-Code',
            'is_superuser':'Human Resource',
            'is_staff' : 'Manager',
            'is_worker':'Worker',
       
        }
        def clean_first_name(self):
            first_name = self.cleaned_data['first_name']
            if not re.match(r'^[a-zA-Z]+$', first_name):
                raise forms.ValidationError('First name should only contain alphabetic characters.')
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data['last_name']
            if not re.match(r'^[a-zA-Z]+$', last_name):
                raise forms.ValidationError('Last name should only contain alphabetic characters.')
            return last_name
        
        def clean_mobile(self):
            mobile = self.cleaned_data['mobile']
            if not re.match(r'^\+[0-9]+$', mobile):
                raise forms.ValidationError('Mobile number should start with "+" and contain only digits.')
            return mobile

        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['role'].required = False
        self.fields['role'].widget.choices[0] = ('', 'Select')
        self.fields['department'].widget.choices[0] = ('', 'Select ')
    
    
  
            
class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


    widgets = {
            'password': PasswordInput(attrs={'type': 'password'})
        }
    class Meta:
        model = User
        fields = ('username','password')
        error_messages = {
            'username':{
                'unique':''
            }
        }
        labels ={
            'username':'Employee-Code',
            'password':'Password'
        }
        
            
class CodeForm(forms.ModelForm):
    number =  forms.CharField(label='Code',required=False)
   
    class Meta:
        model = Code
        fields = ('number',)
            
            
        
        # self.fields['username'].required = False
        # self.fields['role'].empty_label = 'select'
        # self.fields['department'].empty_label = 'select'
        # if self.is_bound and self.is_valid():
        #     if self.cleaned_data.get('department') == 'HR':
        #         self.fields['role'].widget.attrs['disabled'] = 'disabled'
        # self.fields['username'].help_text = None
        # if is_registration:
        #     self.fields['first_name'].required = True
        #     self.fields['last_name'].required = True
        #     self.fields['email'].required = True
        #     self.fields['department'].required = True
        #     self.fields['mobile'].required = True
        # else:
        #     fields_to_delete = []
        #     for field_name in self.fields:
        #         if field_name not in ['username', 'password']:
        #             fields_to_delete.append(field_name)

        #     for field_name in fields_to_delete:
        #         del self.fields[field_name]
        # if not is_registration:
        #     fields_to_delete = ['first_name', 'last_name', 'email', 'department', 'mobile']
        #     for field_name in fields_to_delete:
        #         del self.fields[field_name]
   
            
            
            
# class LoginForm(UserForm):
#     class Meta(UserForm.Meta):
       
#         fields = ('email','password')
    
    
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
# self.fields['username'].help_text = None
      