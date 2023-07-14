from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NoticeboardForm,DepartmentnoticeForm,LeaveForm,TodayTaskForm,PaychequeForm,UserProfileForm
from .models import Notice_board,Department_notice,LeaveApply,TodayTasks,Paycheque,UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from accounts.forms import UserForm
from PIL import Image

# Create your views here.
# @login_required(login_url='login')
def Notice_board_view(request):
    if request.method == 'GET':
        notice_board_list = Notice_board.objects.all()
        return render(request,'dashboard/notice_board.html',{'notice_board_list':notice_board_list}) 
# @login_required(login_url='login')
def Notice_board_hr_crud(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = NoticeboardForm()
        else:
            notice = Notice_board.objects.get(pk=id)
            form = NoticeboardForm(instance=notice)
        return render(request, 'dashboard/notice_board_hrcrud.html', {'form': form})
    else:
        if id == 0:
            form = NoticeboardForm(request.POST,request.FILES)
            
        else:
            notice = Notice_board.objects.get(pk=id)
            form = NoticeboardForm(request.POST,request.FILES,instance=notice)
   
        if form.is_valid():
            print(form)
            notice = form.save(commit=False)
            notice.save()
            
            return redirect('dashboard') 
        # messages.error(request,'hell')  
        return HttpResponse('image size is too big')
          
def Notice_board_hr_delete(request,id):

    if request.method =='POST':
        try:
            notice = Notice_board.objects.get(pk=id)
            notice.delete()
        except  Notice_board.DoesNotExist:
            messages.error(request,'Something Went Wrong')
        return redirect('dashboard')       
        
    return render(request,'dashboard/Delete.html')
                
def Department_notice_view(request):
    if request.method == 'GET':
        department_notices = Department_notice.objects.all()
        return render(request,'dashboard/department_notice.html',{'department_notices':department_notices})
    
    
def Department_notice_crud(request,id=0):
    if request.method == 'POST':  
        if id == 0:
            form = DepartmentnoticeForm(request.POST,request.FILES)
        else:   
            department_notice = Department_notice.objects.get(pk=id)
            form = DepartmentnoticeForm(request.POST,request.FILES,instance = department_notice)
        if form.is_valid():
            form.save()
            return redirect('department_notice_view') 
    else:
        if id == 0:
            form = DepartmentnoticeForm()
        else:
            department_notice = Department_notice.objects.get(pk=id)
            form = DepartmentnoticeForm(instance=department_notice)
        return render(request,'dashboard/department_notice_crud.html',{'form':form})
                         


def Department_notice_delete(request,id=0):
        if request.method == 'POST':
            try:
                department_notice = Department_notice.objects.get(pk=id)
                department_notice.delete()
                return redirect('department_notice_view')
            except Department_notice.DoesNotExist:
                messages.error(request,'Something Went Wrong')
        return render(request,'dashboard/Delete.html')
    

def Leave_user_form(request,id=0):
    
    if request.method == 'POST':
        if id == 0:
            form = LeaveForm(request.POST)            
        else:
            leave = LeaveApply.objects.get(pk=id)
            form = LeaveForm(request.POST,instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            return redirect('leave_view')
        
    else:
        if id == 0:
            form = LeaveForm()
        else:
            leave = LeaveApply.objects.get(pk=id)
            form = LeaveForm(instance = leave)
        return render(request,'dashboard/leave_form.html',{'form':form})
        

def Leave_user_view(request):
    leaves = LeaveApply.objects.all()
    return render(request,'dashboard/leave_view.html',{'leaves':leaves})


def Leave_user_delete(request,id=0):
    if request.method == 'POST':
        leave = LeaveApply.objects.get(pk=id)
        leave.delete()
        return redirect ('leave_form')
    return render(request,'dashboard/Delete.html')



def Today_task_form(request,id=0):
    if request.method == 'POST':
        if id==0:
            form = TodayTaskForm(request.POST)
        else:
            comments = TodayTasks.objects.get(pk=id)
            form = TodayTaskForm(request.POST,instance=comments)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('today_task_view')
        else:
            return HttpResponse('hell')
    else:
        if id == 0:
            form =TodayTaskForm()
        else:
            comments = TodayTasks.objects.get(pk=id)
            form = TodayTaskForm(instance=comments)
        return render(request,'dashboard/today_task_form.html',{'form':form})
    
def Today_task_view(request):
    comments = TodayTasks.objects.all()
    return render(request,'dashboard/today_task_view.html',{'comments':comments})

def Today_task_delete(request,id=0):
    if request.method == 'POST':
        comment = TodayTasks.objects.get(pk=id)
        comment.delete()  
        return redirect('home')  
    return render(request,'dashboard/Delete.html')
            


def Paycheque_form(request,id=0):
    if request.method == 'POST':
        if id == 0:
            form = PaychequeForm(request.POST)
        else:
            cheques = Paycheque.objects.get(pk=id)
            form = PaychequeForm(request.POST,instance=cheques)
        # print('hii')   
        if form.is_valid():
            print(form)
            paycheque = form.save(commit=False)
            paycheque.employer = request.user
        
            # paycheque.updated_at = 
            paycheque.save()
            return render(request,'accounts/confirmation_messages.html')
        else:
            print(form.errors)
            return HttpResponse('hb')
    else:
        if id == 0:
            form = PaychequeForm()
        else:
            cheques = paycheque.objects.get(pk=id)
            form = PaychequeForm(instance=cheques)
        return render (request,'dashboard/paycheque_form.html',{'form':form})
            
def Paycheque_view(request):
    cheques = Paycheque.objects.all()
    return render (request,'dashboard/paycheque_view.html',{'cheques':cheques})

def Paycheque_delete(request,id=0):
    if request.method == 'POST':
        cheques = Paycheque.objects.get(pk=id)
        cheques.delete()
        return redirect('paycheque_form')
    return render(request,'dashboard/Delete.html')





def user_profile_form(request,id=0):
    if request.method == 'POST': 
        userprofile = UserProfile.objects.get(pk=id)
        userprofile_user = User.objects.get(email=userprofile.user.email)
        userform = UserForm(request.POST,instance=userprofile_user)
        profileform = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if userform.is_valid() and profileform.is_valid():
            # profile_picture = profileform.cleaned_data['profile_picture']
            profileform.save()
            userform.save()
            # if profile_form.profile_picture:
                # profile_picture = profileform.cleaned_data.get('profile_picture')  
                # if profile_picture:
                #     profile_form.profile_picture = profile_picture
                # # profile_form.profile_picture = profile_picture
                # print(profile_form.profile_picture)
                #     # img = Image.open(profile_picture)
                #     # if img.height > 85 or img.width > 85:
                #     #     output_size = (85,85)
                #     #     img.thumbnail(output_size)
                # # try:    #     img.save(profile_picture)  
                # # try:
                # profile_form.save()
                # user_form.save()                      
            # except AttributeError:
                
            #     return HttpResponse('user_profile_view')
                 
            return redirect('user_profile_view')
            # except AttributeError:
            #     return HttpResponse(f'something {AttributeError} happened')
        else:
            print(userform.errors)
            print(profileform.errors)
            return HttpResponse('jjj')
    else:
        userprofile = UserProfile.objects.get(pk=id)
        userprofile_user = User.objects.get(email=userprofile.user.email)
        profileform = UserProfileForm(instance=userprofile)
        userform = UserForm(instance=userprofile_user)
        return render(request,'dashboard/user_profile_form.html',{'userform':userform,'profileform':profileform})


def user_profile_form(request, id=0):
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(pk=id)
        userprofile_user = User.objects.get(email=userprofile.user.email)
        userform = UserForm(request.POST, instance=userprofile_user)
        profileform = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if userform.is_valid() and profileform.is_valid():
            # uploaded_file = request.FILES['profile_picture']
            # print(uploaded_file)
            # if uploaded_file:
            #     print(uploaded_file)
                
            user_instance = userform.save(commit=False)
            profile_instance = profileform.save(commit=False)
            user_instance.save()
            profile_instance.user = user_instance
            # profile_instance.profile_picture = uploaded_file                
            # print('kjh',profile_instance.profile_picture)
            profile_instance.save()
            # print('jhgf',profile_instance.profile_picture)
            # print(uploaded_file)
            return redirect('user_profile_view')
            # else:
            #     user_instance = userform.save(commit=False)
            #     profile_instance = profileform.save(commit=False)
            #     user_instance.save()
            #     profile_instance.user = user_instance
            #     profile_instance.profile_picture = None     
                
            #     profileform.save()
            #     return redirect('home')
        else:
            print(userform.errors)
            print(profileform.errors)
            return redirect('user_profile_edit',id)
    else:
        userprofile = UserProfile.objects.get(pk=id)
        userprofile_user = User.objects.get(email=userprofile.user.email)
        profileform = UserProfileForm(instance=userprofile)
        userform = UserForm(instance=userprofile_user)
        return render(request, 'dashboard/user_profile_form.html', {'userform': userform, 'profileform': profileform})

  
def user_profile_view(request):
    user_profiles = UserProfile.objects.all()
    return render (request,'dashboard/user_profile_view.html',{'user_profiles':user_profiles})

def user_profile_delete(request,id=0):
    if request.method =='POST':
        userprofile = UserProfile.objects.get(pk=id)
        userprofile_user = User.objects.get(email=userprofile.user.email)
        userprofile_user.delete()
        return redirect ('user_profile_view')
    return render (request,'dashboard/Delete.html')