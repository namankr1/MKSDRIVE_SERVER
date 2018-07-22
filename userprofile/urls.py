from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/',views.signin, name='signin'),
    path('verifyotp/', views.verifyOTP, name='verifyotp'),
    path('signout/', views.signout, name='signout'),
    path('sendotp/', views.sendOTP, name='sendotp'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('checkversion/', views.checkversion, name='checkversion'),
    path('updatefolderid/', views.updatefolderid, name='updatefolderid'),
    path('getprofile/', views.getprofile, name='getprofile')
    ] 
