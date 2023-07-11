from django.urls import path
from . import views


urlpatterns = [
    path('',views.Notice_board_view,name='dashboard'),
    path('notice_hr_create/',views.Notice_board_hr_crud,name='notice_hr_create'),
    path('notice_hr_edit/<int:id>/',views.Notice_board_hr_crud,name='notice_hr_edit'),
    path('notice_hr_delete/<int:id>/',views.Notice_board_hr_delete,name='notice_hr_delete'),
    path('department_notice_view/',views.Department_notice_view,name='department_notice_view'),
    path('department_notice_create/',views.Department_notice_crud,name='department_notice_create'),
    path('department_notice_edit/<int:id>',views.Department_notice_crud,name='department_notice_edit'),
    path('department_notice_delete/<int:id>',views.Department_notice_delete,name='department_notice_delete'),
    path('leave_view/',views.Leave_user_view,name='leave_view'),
    path('leave_form/',views.Leave_user_form,name='leave_form'),
    path('leave_form_edit/<int:id>',views.Leave_user_form,name='leave_form_edit'),
    path('leave_form_delete/<int:id>',views.Leave_user_delete,name='leave_form_delete'),
] 



