from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('login',views.login,name="home"),
    path('otpverify',login_required(views.otpverify),name="otpverify"),
    path('resend',login_required(views.resend_otp),name="uhome"),

    path('home',login_required(views.home),name="uhome"),
    path('profile/delete/<slug:slug>',login_required(views.delete_user),name="delete"),
    path('logout',login_required(views.logout),name='logout'),
    path('files/delete/<slug:slug>',login_required(views.file_delete),name='file_delete'),
    #path('tfiles/update/<slug:>slug',login_required(views.allfiles),name='upfile'),
    path('files',login_required(views.allfiles),name='upfile'),
    path('notifications',login_required(views.t_notification_home),name='logout'),
    path('notifications/<slug:slug>',login_required(views.t_notification_handle),name='t_notification_handle'),
    path('notifications/delete/<slug:slug>',login_required(views.t_notification_delete),name='t_notification_delete'),
    path('tup_file',login_required(views.tup_file),name='tup_file'),
    path('profile',login_required(views.profile),name='profile'),
    path('profile/<slug:slug>',login_required(views.view_profile_a),name='view_profile_a'),
    path('upload_pic',login_required(views.upload_pic_a),name='uplaod_pic_a'),
]