from django.shortcuts import render,redirect
from .forms import UserForm,LoginForm
from .models import User
from django.http import HttpResponse
from django.contrib import messages
import secrets
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import check_password

#email sending
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

def Registration(request):
    
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():          
            print('hii1')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile = form.cleaned_data['mobile']
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            try :
                user = User.objects.get(email=email)
                form.add_error('email','Same Email With User Already exist')
            except User.DoesNotExist:
                if User.objects.filter(mobile=mobile).exists():
                    form.add_error('mobile', 'User with the same mobile number already exists')
                elif len(mobile) != 10 or not mobile.isdigit():
                    form.add_error('mobile', 'Please enter a valid 10-digit mobile number')
                    
      
                else:
                        user = form.save(commit=False)  
                        user.mobile = mobile
                        username_id = secrets.token_hex(2)            
                        username = f"{first_name[:2]}{username_id}{last_name[:2]}".upper()
                        # username = username_create.upper()
                        user.username=username
                        # print(user.username)
                        temporary_password = secrets.token_urlsafe(10)
                        # hashed_password = make_password(temparory_password)
                        #SENDING EMAIL
                        current_site = get_current_site(request) 
                        mail_subject = "Welcome to the company,here's your id and password to login" 
                        message = render_to_string('accounts/login_id_pass.html',{
                            'user':user,
                            'password':temporary_password,
                            'domain':current_site,
                            # 'uid':urlsafe_base64_encode(force_bytes(user.pk))
                        })
                        to_email = email
                        try:
                            send_email = EmailMessage(mail_subject,message,to=[to_email])
                            send_email.send()
                        except:
                            messages.error(request,'email not send')
                        password = make_password(temporary_password)
                        user.password = password
                        print('hii')
                        user.save()
                        print(user.save())
                        
                        messages.success(request,'Registration Succesfull') 
    context ={
        'form':form,
        }  

    return render(request, 'accounts/register.html', context)    


# def loginPage(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             # Check if a user with the given email exists
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 user = None

#             # Authenticate the user using the email and password
#             if user is not None:
#                 user = authenticate(request, username=user.username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, 'Logged in successfully')
#                     return redirect('login')
            
#             # If authentication fails, show an error message
#             messages.error(request, "Invalid email or password")
#     else:
#         form = UserForm()
    
#     context = {'form': form}
#     return render(request, 'accounts/login.html', context)


@never_cache
def loginPage(request):
    
    # User = get_user_model()
    if request.method == 'POST':
     
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('post')
        user = authenticate(request,username=username,password=password)
        print('post1')
        # print(user.username)
        print(user)

        # password = '11uhIrxEk7zbOA'
        # stored_hash = 'pbkdf2_sha256$600000$ConuhQZ5X9Nns0uIl5bo6g$/3AXLA6c/F8gEwH/rL4GXl+i+o6c0izq496wRhwwS6w='

        # if check_password(password, stored_hash):
        #     print('Password is correct.')
        # else:
        #      print('Password is incorrect.')

        if user is not None:
            print('uu') 
            if user.is_superuser:
                # print('yoo')   
                login(request,user)
                return redirect('home')  
            elif  user.last_login is None:
                return redirect('resetpassword',id=user.id)
            else:
                login(request,user)
                messages.success(request,'und')
                return redirect('home')

        else:
            messages.error(request,'illa')
        
    #     if form.is_valid():
    #         print('in')
    #         email = form.cleaned_data['email']
    #         password = form.cleaned_data['password']
    #         print(email)
    #         print(password)
            
    #         user = authenticate(request,email=email,password=password)
    #         print(user)
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, 'Logged in successfully')
    #         else:
    #             messages.error(request, "User doesn't exist")
    #     else:
    #         # username = form.cleaned_data['username']
    #         # password = form.cleaned_data['password']
            
    #         # user = authenticate(request, username=username, password=password)
    #         # if user is not None:
    #         #     login(request, user)
    #         #     messages.success(request, 'Logged in successfully')
    #         # else:
    #         #     messages.error(request, "User doesn't exist")
    #         messages.error(request, 'Invalid form')
    #         # return HttpResponse('hh')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@never_cache
def homePage(request):
    return HttpResponse('hii') 

@never_cache
def reset_password(request,id=0):
    if request.method == 'POST':
        password = request.POST.get('password')
        Cpassword = request.POST.get('Cpassword')
        try:
            user = User.objects.get(id=id)
            if password == Cpassword:
                user.set_password(password)
                user.save()
                #sending email for reset password
                current_site = get_current_site(request)
                mail_subject = 'reset password'
                message = render_to_string('accounts/reset_password_verification.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user)    #creating the token for specific user
                    
                })
                to_email = user.email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                messages.success(request,'We Send You a Verification Link to your mail address , please confirm that ')
                
            else:
                messages.error(request,'password not matching')
                
        except User.DoesNotExist:
            pass
        
        
        
    return render(request,'accounts/reset_password.html')

def verify(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(user)
    except (User.DoesNotExist,TypeError,ValueError,OverflowError):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.save()
        # messages.success(request,'congratulations')
        login(request,user)
        return redirect('home')
    else:
        messages.error(request,'error')
        return redirect ('login')
        