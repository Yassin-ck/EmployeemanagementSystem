from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NoticeboardForm,DepartmentnoticeForm,LeaveForm,TodayTaskForm,PaychequeForm
from .models import Notice_board,Department_notice,LeaveApply,TodayTasks,Paycheque
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