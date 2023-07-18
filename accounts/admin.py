from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','role','department')


class CodeAdmin(admin.ModelAdmin):
    list_display = ('user','number')
    
    
admin.site.register(User,UserAdmin)
admin.site.register(Code,CodeAdmin)
# admin.site.register(Department)

