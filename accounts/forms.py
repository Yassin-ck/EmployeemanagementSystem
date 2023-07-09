from django import forms
from django.forms import PasswordInput
from .models import User,Code

class UserForm(forms.ModelForm):
    country_code = forms.CharField(max_length=4)
    mobile = forms.CharField(max_length=10,help_text='Use a valid Mobile number with correct Country Code')
    class Meta:
        model = User
        
        fields = ('first_name','last_name','email','role','department','mobile','country_code','username')
                  
        error_messages = {
            'mobile':{
                'unique':'User with this  Mobile Number  already exists.'
            },
            'username':{
                'unique':'User with this EmployeeCode already exists'
            }
        }
        labels = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'email':'Email',
            'role':'Role',
            'department':'Department',
            'country_code': '',
            'mobile':'Mobile Number',
            'username':'Employee-Code'
            
        }
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['role'].required = False
        self.fields['role'].widget.choices[0] = ('', 'Select')
        self.fields['department'].widget.choices[0] = ('', 'Select ')
    
    
  
            
class LoginForm(forms.ModelForm):
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
    number =  forms.CharField(label='Code',help_text='Enter SMS Verification Code',required=False)
   
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
      