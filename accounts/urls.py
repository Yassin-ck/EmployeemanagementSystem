from django.urls import path
from . import views

urlpatterns = [
    # path('check-failed-attempts/', views.check_failed_attempts, name='check_failed_attempts'),
    path('register/',views.Registration,name='register'),
    path('',views.loginPage,name='login'),
    path('logout/',views.loginPage,name='logout'),
    path('home/',views.homePage,name='home'),
    path('resetpassword/<int:id>/',views.reset_password,name='resetpassword'),
    path('verify/<uidb64>/<token>/',views.verify,name='verify'),
    path('passwordresetemail/<int:id>', views.EmialPassowrdreset,name='passwordresetemail'),
    path('emailpassid/', views.Login_Id_Pass_email,name='emailpassid'),
    path('resetpasswordemailverification/', views.resetpasswordemail_verificationPage,name='resetpasswordemailverification'),
    path('twoFactorAuthentication/', views.TwoFactorAuthentication,name='twoFactorAuthentication'),
]
 