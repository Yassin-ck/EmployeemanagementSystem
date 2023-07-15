from django.contrib import admin
from .models import Notice_board,Department_notice,LeaveApply,TodayTasks,Paycheque,UserProfile

# Register your models here.

admin.site.register(Notice_board)
admin.site.register(Department_notice)
admin.site.register(LeaveApply)
admin.site.register(TodayTasks)
admin.site.register(Paycheque)
admin.site.register(UserProfile)
