from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('x',views.xhome,name="home"),
    path('message',views.msg_to_admin,name="home")
]