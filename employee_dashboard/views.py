from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NoticeboardForm,DepartmentnoticeForm,LeaveForm,PaychequeForm,UserProfileForm,TodayTaskForm
from .models import Notice_board,Department_notice,LeaveApply,TodayTasks,Paycheque,UserProfile
from django.contrib import messages
from accounts.models import User
from accounts.forms import UserForm
from PIL import Image
from django.shortcuts import get_object_or_404
from employeemanagmentsystem.decorators import allowed_users,dashboard_authentication
from django.views.decorators.cache import never_cache
from django.urls import path



# Create your views here.

@dashboard_authentication
def Notice_board_view(request):
    notice_boards = Notice_board.objects.all()
    return render (request,'dashboard/notice_board.html',{'notice_boards':notice_boards})

# @dashboard_authentication
# def Notice_board_single_view(request, id=0):
#     notice_board = Notice_board.objects.get(pk=id)
#     comments = notice_board.notice_board_comment.all().order_by('-created_at')
#     print(notice_board)
#     print(comments)
#     notice = get_object_or_404(Notice_board, pk=id)
#     if request.method == 'POST':
#         comment=request.POST.get('comment')
#         if comment:
#             comment_instance = TodayTasks.objects.create(
#                 user=request.user,
#                 notice_board = notice_board ,
#                 comment=comment
#             )
#         return redirect('dashboard_single',id=notice_board.id)       
#     return render(request, 'dashboard/hr_depart_notice_single.html', {'notice': notice, 'comments': comments})
     


@allowed_users(allowed_roles=['HumanResource'])
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
            # print(form)
            notice=form.save(commit=False)
            notice.save()
            
            return redirect('dashboard') 
        # messages.error(request,'hell')  
        return HttpResponse('image size is too big')
    
@allowed_users(allowed_roles=['HumanResource'])         
def Notice_board_hr_delete(request,id):

    if request.method =='POST':
        try:
            notice = Notice_board.objects.get(pk=id)
            notice.delete()
        except  Notice_board.DoesNotExist:
            messages.error(request,'Something Went Wrong')
        return redirect('dashboard')       
        
    return render(request,'dashboard/Delete.html')
    
                
@dashboard_authentication
def Department_notice_view(request):  
    department_notices = Department_notice.objects.all()
    return render(request,'dashboard/department_notice.html',{'department_notices':department_notices})
 
 
# @dashboard_authentication
# def Department_notice_single_view(request, id=0):   
#     notices = Department_notice.objects.get(pk=id)
#     comments_dept = notices.department_comment.all().order_by('-created_at')
 
#     if request.method == 'POST':
#         department_instance = TodayTasks.objects.create(
#             user=request.user,
#             department_notice_board=notices,
#             comment=request.POST.get('comment')
#         )
#         return redirect('department_notice_single_view', id=notices.id)

#     return render(request, 'dashboard/dept_notice_single.html', {'notices': notices, 'comments_dept': comments_dept})

    
   
@allowed_users(allowed_roles=['manager'])         
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
                         


@allowed_users(allowed_roles=['manager'])         
def Department_notice_delete(request,id=0):
        if request.method == 'POST':
            try:
                department_notice = Department_notice.objects.get(pk=id)
                department_notice.delete()
                return redirect('department_notice_view')
            except Department_notice.DoesNotExist:
                messages.error(request,'Something Went Wrong')
        return render(request,'dashboard/Delete.html')
    

@dashboard_authentication
def Leave_user_form(request,id=0): 
    user_leave = LeaveApply.objects.filter(user=request.user) 
    if user_leave.exists() and user_leave[0].status == 'Pending' :
        messages.error(request,'Your Leave Request is Pending ')
        return redirect('leave_personal_view',id=request.user.id)
    else:
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
                return redirect('leave_personal_view',id=leave.user.id)
            
        else:
            if id == 0:
                form = LeaveForm()
            else:
                leave = LeaveApply.objects.get(pk=id)
                form = LeaveForm(instance = leave)
            return render(request,'dashboard/leave_form.html',{'form':form})
            

@dashboard_authentication
def Leave_user_view(request,id=0):
    if id == 0:
        if request.user.is_superuser:
            leaves = LeaveApply.objects.filter(status='Pending')
        else:
            return redirect('home')
    else:
        user = get_object_or_404(User,pk=id)
        leaves = LeaveApply.objects.filter(user=user)
        
    return render(request,'dashboard/leave_view.html',{'leaves':leaves})


# def Leave_filtered(request):
#     leaves_filterted = LeaveApply.objects.filter(status__exact='Pending')
#     return render(request,'dashboard/leave_view.html',{'leave_filtered':leaves_filterted})



@never_cache
def Leave_user_delete(request,id=0):
    if request.method == 'POST':
        leave = LeaveApply.objects.get(pk=id)
        leave.delete()
        return redirect ('leave_form')
    return render(request,'dashboard/Delete.html')


@allowed_users(allowed_roles=['HumanResource'])
def Leave_approval_rejection(request,id):
    leave_request = LeaveApply.objects.get(pk=id)
    if 'leave_approval' in request.path:
        leave_request.status = 'Approved'
        leave_request.approved_by_hr = request.user
    else:
        leave_request.status = 'Rejected'
        leave_request.approved_by_hr = request.user
    leave_request.save()
    return redirect('leave_view')
        
    

@allowed_users(allowed_roles=['worker'])
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
            return redirect('today_task_view',id=request.user.id)
        else:
            return HttpResponse('hell')
    else:
        if id == 0:
            form =TodayTaskForm()
        else:
            comments = TodayTasks.objects.get(pk=id)
            form = TodayTaskForm(instance=comments)
        return render(request,'dashboard/today_task_form.html',{'form':form})
    
@allowed_users(allowed_roles=['worker','manager'])
@dashboard_authentication
def Today_task_view(request, id=0):
        if id == 0:
            today_tasks = TodayTasks.objects.all()
        else:
            user = User.objects.get(pk=id)   
            today_tasks = TodayTasks.objects.filter(user=user) 
        return render(request, 'dashboard/today_task_view.html', {'today_tasks': today_tasks})


def Today_task_delete(request,id=0):
    if request.method == 'POST':
        tasks = TodayTasks.objects.get(pk=id)
        tasks.delete()  
        return redirect('home')  
    return render(request,'dashboard/Delete.html')
            


@allowed_users(allowed_roles=['HumanResource'])         
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
            # payc
            paycheque.salary = Paycheque.Total_salary(paycheque)
            paycheque.save()
            return render(request,'accounts/confirmation_messages.html')
        else:
            print(form.errors)
            return HttpResponse('hb')
    else:
        if id == 0:
            form = PaychequeForm()
        else:
            cheques = Paycheque.objects.get(pk=id)
            form = PaychequeForm(instance=cheques)
        return render (request,'dashboard/paycheque_form.html',{'form':form})

    


            
@dashboard_authentication
def Paycheque_view(request,id=0):
    if id == 0: 
        cheques = Paycheque.objects.all()
    else:
        user = get_object_or_404(User,pk=id)
        cheques = Paycheque.objects.filter(user=user) 
    return render (request,'dashboard/paycheque_view.html',{'cheques':cheques})

def Paycheque_delete(request,id=0):
    if request.method == 'POST':
        cheques = Paycheque.objects.get(pk=id)
        cheques.delete()
        return redirect('paycheque_form')
    return render(request,'dashboard/Delete.html')





@allowed_users(allowed_roles=['HumanResource'])         
def user_profile_form(request, id=0):
    if request.method == 'POST':
        userprofile = get_object_or_404(UserProfile, pk=id)
        userprofile_user = userprofile.user
        userform = UserForm(request.POST, instance=userprofile_user)
        profileform = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if userform.is_valid() and profileform.is_valid():
            empcode = userform.cleaned_data['username']
            if len(empcode) < 5:
                userform.add_error('username', 'Username should be at least 5 characters long.')
            if not userform.errors and not profileform.errors :
                   
                user_instance = userform.save(commit=False)
                profile_instance = profileform.save(commit=False)
                user_instance.save()
                profile_instance.user = user_instance
                user_instance.save()
                profile_instance.save()
                return redirect('user_profile_single_view',id)
            else:
                print(userform.errors)
                print(profileform.errors)
                return render(request, 'dashboard/user_profile_form.html', {'userform': userform, 'profileform': profileform})
        else:
            print(userform.errors)
            print(profileform.errors)
            return render(request, 'dashboard/user_profile_form.html', {'userform': userform, 'profileform': profileform})
    else:
        userprofile = get_object_or_404(UserProfile, pk=id)
        userprofile_user = userprofile.user
        profileform = UserProfileForm(instance=userprofile)
        userform = UserForm(instance=userprofile_user)
        return render(request, 'dashboard/user_profile_form.html', {'userform': userform, 'profileform': profileform})


  
@dashboard_authentication
def user_profile_view(request,id=0):
    if id==0:
        if request.user.is_superuser:
            user_profiles = UserProfile.objects.all()
            return render (request,'dashboard/user_profile_view.html',{'user_profiles':user_profiles})
        else:
            return redirect('home')
    else:
        user_profile = UserProfile.objects.get(pk=id)
        return render (request,'dashboard/user_profile_single_view.html',{'user_profile':user_profile})

@allowed_users(allowed_roles=['HumanResource'])         
def user_profile_delete(request,id=0):
    if request.method =='POST':
        userprofile = UserProfile.objects.get(pk=id)
        userprofile_user = User.objects.get(email=userprofile.user.email)
        userprofile_user.delete()
        return redirect ('user_profile_view')
    return render (request,'dashboard/Delete.html')


