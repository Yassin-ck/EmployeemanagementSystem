from django.contrib import admin
from .models import Notice_board,Department_notice,LeaveApply

# Register your models here.

admin.site.register(Notice_board)
admin.site.register(Department_notice)
admin.site.register(LeaveApply)