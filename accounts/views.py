from django.shortcuts import render,redirect
from .forms import UserForm,LoginForm,CodeForm
from .models import User
from django.http import HttpResponse
from django.contrib import messages
import secrets
import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
# OTP Verification
from .utils import send_sms
#email sending
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
#Blocking user After 3 failed Login Attempt
from BruteBuster.models import FailedAttempt
from Dashboard.models import UserProfile
# from django.utils  import timezone 

# Create your views here.
# @login_required(login_url='login')
def homePage(request):
    return render(request,'accounts/home.html')

def Registration(request):
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        print('hii4')
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile = form.cleaned_data['mobile']
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            employeeCode = form.cleaned_data['username']
            print('hii')
            try:
                print('hii1')
                User.objects.get(email=email)
                form.add_error('email', 'User with the same email already exists')
            except User.DoesNotExist:
                try:
                    print('hii2')
                    User.objects.get(username=employeeCode.upper())
                    messages.error(request, 'EmployeeCode already in use')
                except User.DoesNotExist:
                    print('hii3')
                    if len(mobile) <= 12 and re.match(r'^\+\d+$', mobile):
                        form.add_error('mobile', 'Please enter a valid mobile number with CountryCode (e.g., +1234567890)')
                        print('kk')
                    else:
                        print('jhgf')
                        user = form.save(commit=False)
                        # user.date_joined = timezone.now()
                        user.username = employeeCode.upper()
                        temporary_password = secrets.token_urlsafe(10)
                        current_site = get_current_site(request)
                        mail_subject = "Welcome, Here's Your EmployeeCode and Password to Login..."
                        message = render_to_string('accounts/login_id_pass.html', {
                            'user': user,
                            'password': temporary_password,
                            'domain': current_site,
                        })
                        to_email = email
                        try:
                            send_email = EmailMessage(mail_subject, message, to=[to_email])
                            send_email.send()
                            password = make_password(temporary_password)
                            user.password = password
                            user.save()
                            profile = UserProfile()
                            profile.user_id = user.id
                            profile.profile_picture = 'userprofile/default.profilepicture.jpg'
                            profile.save()
                            return redirect('emailpassid')
                        except:
                            messages.error(request, 'Email not sent')

                        
        else:
            print(form.errors)
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)   



@never_cache
def loginPage(request):
    
    if request.method == 'POST':
     
        form = LoginForm(request.POST)
        EmployeeCode = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=EmployeeCode,password=password)
        
        if user is not None:
            if user.is_superuser or user.last_login is not None:
                request.session['pk']=user.pk
                return redirect('twoFactorAuthentication')  
            else:
                return redirect('passwordresetemail',id=user.id)
            

        else:
            form.add_error('username','')
            form.add_error('password','')
            
            user = FailedAttempt.objects.get(username = EmployeeCode)
            user_blocked = user.blocked()
            if user_blocked:
                messages.error(request,f"""Your Account Has Been Blocked...
                               Try Again After Sometimes""")
            else:
                messages.error(request,f"""Incorrect Id or Password!!!  
                  You tried {user.failures} Attempts""")
           
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@never_cache

def reset_password(request,id=0):
    if request.method == 'POST':
        password = request.POST.get('password')
        Cpassword = request.POST.get('Cpassword')
        try:
            user = User.objects.get(id=id)
            if password == Cpassword and len(password)<=6:
                
                user.set_password(password)
          
                user.save()
                # if user.verify():
                login(request,user)
                return redirect('home')
                
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
        return redirect('resetpassword',id=user.id)
    else:
        messages.error(request,'Error occurred while Activating')
        return redirect ('login')
     
def EmialPassowrdreset(request,id=0):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user=User.objects.get(pk=id)
            current_site = get_current_site(request)
            mail_subject = 'reset password' 
            message = render_to_string('accounts/reset_password_verification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)    #creating the token for specific user      
                })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('resetpasswordemailverification')
        except User.DoesNotExist:
            messages.error(request,'Unauthorized Entry caught')
            
        
    return render(request,'accounts/email_reset_password.html')

def Login_Id_Pass_email(request):
    messages.success(request,'Email Sended Succesfully') 

    return render(request,'accounts/confirmation_messages.html')


def resetpasswordemail_verificationPage(request):
    messages.success(request,'We Send You a Verification Link to your mail address , please confirm that ')

    return render(request,'accounts/confirmation_messages.html') 


def TwoFactorAuthentication(request):               
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code 
        code_user = f"{user.username} : {code}"
        if not request.POST:
            try:
                send_sms(code_user,user.mobile)    
                messages.success(request,'We send you a OTP to the registerd Mobile Number')
            except:
                messages.error(request,'Error ocuured while we sending the OTP to your Mobile Number!!! please Retry...')
                
            print(code_user)           
        if form.is_valid():
            
            number =form.cleaned_data.get('number')
            
            if str(code) == number:
                # print(number)
                code.save()
                login(request,user)                              
                return redirect('home')
            else:
                messages.error(request,'Invalid OTP number')
                
    return render(request,'accounts/twofactor_auth.html',{'form':form})
           
def logout(request):
    logout(request)
    return redirect('home')
    