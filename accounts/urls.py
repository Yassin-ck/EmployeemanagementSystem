from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Registration,name='register'),
    path('',views.loginPage,name='login'),
    path('home/',views.homePage,name='home'),
    path('resetpassword/<int:id>/',views.reset_password,name='resetpassword'),
    path('verify/<uidb64>/<token>/',views.verify,name='verify')
]