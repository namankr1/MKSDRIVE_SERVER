from django.urls import path
from . import views

urlpatterns = [
    path('getdata/', views.getdata, name='getdata'),
    # path('test/', views.test, name='test'),
    path('senddata/', views.senddata, name='senddata'),
    path('sendmail/', views.sendmail, name='sendmail')
    ]