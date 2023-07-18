from django.contrib import admin
from .models import Notice_board,Department_notice,LeaveApply,TodayTasks,Paycheque,UserProfile

# Register your models here.

class NoticeBoardAdmin(admin.ModelAdmin):
    list_display = ('title','subject','content','image')
    
    
    
class DepartmentNoticeAdmin(admin.ModelAdmin):
    list_display = ('title','subject','content','image')
    
    

class LeaveApplyAdmin(admin.ModelAdmin):
    list_display = ('user','start_date','end_date','reason')
    
    
# class TodayTasksAdmin(admin.ModelAdmin):
#     list_display = ('__str__',)

    

# class PaychequeAdmin(admin.ModelAdmin):
#     list_display = ('__str__',)


        

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','income','city','experience')

admin.site.register(Notice_board,NoticeBoardAdmin)
admin.site.register(Department_notice,DepartmentNoticeAdmin)
admin.site.register(LeaveApply,LeaveApplyAdmin)
admin.site.register(TodayTasks)
admin.site.register(Paycheque)
admin.site.register(UserProfile,UserProfileAdmin)
