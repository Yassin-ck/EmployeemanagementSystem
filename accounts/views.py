from django.shortcuts import render,redirect
from .forms import UserForm,LoginForm,CodeForm,DepartmentHrForm
from .models import User
from django.http import HttpResponse
from django.contrib import messages
import secrets
import re
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
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
# from BruteBuster.models import FailedAttempt
from employee_dashboard.models import UserProfile
# from django.utils  import timezone 

# authentication
from django.contrib.auth.models import Group
from employeemanagmentsystem.decorators import unauthenticated_user,allowed_users


from django.db.models import Max
# Create your views here.
@login_required(login_url='login')
def homePage(request):
    return render(request,'accounts/home.html')


@allowed_users(allowed_roles=['HumanResource'])
def Registration(request):
    hr_superuser = request.user.is_authenticated and request.user.is_superuser
    if request.method == 'GET':
        form = UserForm(superuser=hr_superuser)
    else:
        form = UserForm(request.POST,superuser=hr_superuser)
        print('hii4')
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            mobile = form.cleaned_data['mobile']
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            # employeeCode = form.cleaned_data['username']
            print('hii')
            try:
                print('hii1')
                User.objects.get(email=email)
                messages.error(request, 'User with the same email already exists')
            except User.DoesNotExist:
                # try:
                #     print('hii2')
                #     # User.objects.get(username=employeeCode.upper())
                #     # messages.error(request, 'EmployeeCode already in use')
                # except User.DoesNotExist:
                print('hii3')
                if len(mobile) <= 12 and re.match(r'^\+\d+$', mobile):
                    form.add_error('mobile', 'Please enter a valid mobile number with CountryCode (e.g., +1234567890)')
                    print('kk')
                else:
                    print('jhgf')
                    user = form.save(commit=False)
                    # user.date_joined = timezone.now()
                    # user.username = employeeCode.upper()
                    last_id = User.objects.aggregate(last_id=Max('id'))['last_id']
                    next_id = last_id+1
                    user.username = f"EMP{str(next_id).zfill(3)}"
                    user.department = request.user.department
                    if request.user.department == User.Department.FRONTEND:
                        user.is_frontend = True
                    elif request.user.department == User.Department.BACKEND:
                        user.is_backend =True
                    else:
                        user.is_testing = True
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
                        print('fff')
                        send_email = EmailMessage(mail_subject, message, to=[to_email])
                        send_email.send()    
                        print('fff')
                        password = make_password(temporary_password)
                        user.password = password
                        
                        print(user.username)
                        print(next_id)

                        print('fff')
                        
                        user.save()
                            
                        if user.role == User.Role.HR:    
                            user.is_hr = True                                                        
                            hr_group = Group.objects.get(name='HumanResource')                            
                            print(hr_group)
                            user.groups.add(hr_group) 
                        elif user.role == User.Role.MANAGER:
                            user.is_manager = True                            
                            manager_group = Group.objects.get(name='manager')
                            user.groups.add(manager_group)
                            print('fghhjbs')
                        else:
                            user.is_worker = True
                            worker_group = Group.objects.get(name='worker')
                            user.groups.add(worker_group)
                        user.save()
    
                        profile = UserProfile()
                        print('jhg')
                        profile.user_id = user.id
                        print('jjj')
                        profile.save()
                        print('oihghgjkh')
                        if user.role == User.Role.HR:
                            user.is_active = False
                            user.is_testing =False
                            user.is_backend =False
                            user.is_frontend =False
                            user.save()
                           
                            return redirect('hr_departmenting',id=user.id)
                        return redirect('emailpassid')

                    except:
                        messages.error(request, 'Email not sent')
                       
                        
        else:
            print(form.errors)
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)   


def Hr_departmenting(request,id=0):
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = DepartmentHrForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            user.department = department
            user.is_active = True
            if user.department == User.Department.FRONTEND:
                user.is_frontend = True
            elif user.department == User.Department.BACKEND:
                user.is_backend =True
            else:
                user.is_testing = True
            user.save()
            return redirect('emailpassid')
        else:
            user.delete()
            return redirect('register')
    form = DepartmentHrForm()
    return render(request,'accounts/hr_departmenting.html',{'form':form})
        # department = request.POST.get('department')
        
    


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        EmployeeCode = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=EmployeeCode, password=password)
        print(user)
        if user is not None:
            if user.last_login is None and not user.is_superuser:
                # First login after registration, redirect to reset password
                return redirect('passwordresetemail',id = user.id)
            else:
                user.is_active = False
                user.save()
                # Regular login, redirect to two-factor authentication
                request.session['pk'] = user.pk
                return redirect('twoFactorAuthentication')

        else:
            form.add_error('username', '')
            form.add_error('password', '')
            messages.error(request,'You Are Not Authenticated')    


            # user = FailedAttempt.objects.get(username=EmployeeCode)
            # user_blocked = user.blocked()
            # if user_blocked:
            #     messages.error(request, """Your Account Has Been Blocked...
            #                        Try Again After Sometimes""")
            # else:
            #     messages.error(request, f"""Incorrect Id or Password!!!  
            #           You tried {user.failures} Attempts""")

    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)



def reset_password(request,id=0):
    if request.method == 'POST':
        password = request.POST.get('password')
        Cpassword = request.POST.get('Cpassword')
        try:
            user = User.objects.get(id=id)
            if password == Cpassword and len(password)<=6:
                
                user.set_password(password)
                user.is_active = True
                user.save()
                login(request,user)
                # request.session['user'] = user
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
        user = User.objects.get(pk=id)
        print(user)
        if email == user.email:
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
                user.is_active = False
                send_email.send()
                return redirect('resetpasswordemailverification')
            except User.DoesNotExist:
                messages.error(request,'Unauthorized Entry caught')
        else:
            user.save()
            return redirect ('login')
            
        
    return render(request,'accounts/email_reset_password.html')

def Login_Id_Pass_email(request):
    messages.success(request,'Email Sended Succesfully') 

    return render(request,'accounts/confirmation_messages.html')


def resetpasswordemail_verificationPage(request):
    messages.success(request,'We Send You a Verification Link to your mail address , please confirm that ')

    return render(request,'accounts/confirmation_messages.html') 


def TwoFactorAuthentication(request): 
    pk = request.session.get('pk')
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()              
    form = CodeForm(request.POST or None)
    if pk:
        code = user.code 
        code_user = f"{user.username} : {code}"
        if not request.POST:
            try:
                send_sms(code_user,user.mobile)    
                messages.success(request,'We send you a OTP to the registerd Mobile Number')
            except:
                messages.error(request,f'Error ocuured while we sending the OTP to your Mobile Number!!! please Retry...{code}')
                
            print(code_user)           
        if form.is_valid():
            
            number =form.cleaned_data.get('number')
            
            if str(code) == number:
                # print(number)
                code.save()
                user.is_active =True
                user.save()
                login(request,user)                              
                return redirect('home')
            else:
                user.is_active=False
                user.save()
                messages.error(request,'Invalid OTP number')
                
    return render(request,'accounts/twofactor_auth.html',{'form':form})
          
def logoutPage(request):
    print(request.user)
    # request.user.is_active = False
    logout(request)
    return redirect('login')
    

