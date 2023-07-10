from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Notice_board_view,name='dashboard'),
    path('notice_hr_create/',views.Notice_board_hr_crud,name='notice_hr_create'),
    path('notice_hr_edit/<int:id>/',views.Notice_board_hr_crud,name='notice_hr_edit'),
    path('notice_hr_delete/<int:id>/',views.Notice_board_hr_delete,name='notice_hr_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



