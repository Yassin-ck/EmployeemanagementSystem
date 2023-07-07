from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    
    class Meta:
        model = User
        
        fields = ('first_name','last_name','email','role','department','mobile',
                #   'username','password'
                  )
        error_messages = {
            'mobile':{
                'unique':'This mobile number is already exist'
            }
        }
        labels = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'email':'Email',
            'role':'Role',
            'department':'Department',
            'mobile':'Mobile Number',
            # 'password':'Password',
            # 'username':'Username'
            
            
        
        }
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['role'].required = False
        self.fields['role'].empty_label = 'select'
        self.fields['department'].empty_label = 'select'
            
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
        error_messages = {
            'username':{
                'unique':''
            }
        }
        
        # def __init__(self,*args,**kwargs):
        #     super().__init__(*args,**kwargs)
            
            
       
            
            
        
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
      