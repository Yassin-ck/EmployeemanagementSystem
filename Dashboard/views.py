from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NoticeboardForm,DepartmentnoticeForm,LeaveForm
from .models import Notice_board,Department_notice,LeaveApply
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
            form.save()
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