from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NoticeboardForm
from .models import Notice_board
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# @login_required(login_url='login')
def Notice_board_view(request):
    if request.method == 'GET':
        notice_board_list = Notice_board.objects.all()
    return render(request,'dashboard/notice_board.html',{'notice_board_list':notice_board_list}) 
# @login_required(login_url='login')
from django.shortcuts import render, redirect
from .forms import NoticeboardForm
from .models import Notice_board

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
            form = NoticeboardForm(request.POST)
            
        else:
            notice = Notice_board.objects.get(pk=id)
            form = NoticeboardForm(request.POST,instance=notice)
        if form.is_valid():
           form.save()
        return redirect('dashboard')   

def Notice_board_hr_delete(request,id):
    form = NoticeboardForm()
    if request.method =='POST':
        try:
            notice = Notice_board.objects.get(pk=id)
            notice.delete()
        except  Notice_board.DoesNotExist:
            messages.error(request,'Something Went Wri\ong')
        return redirect('dashboard')
            
        
    return render(request,'dashboard/Delete.html',{'form':form})
        
                 
        
    
    

        
        
    

