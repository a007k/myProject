

from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path('login',views.tlog,name="home"),
    path('otpverify',login_required(views.totpverify),name="uhome"),
    path('resend',login_required(views.t_resend_otp),name="uhome"),
    path('home',login_required(views.thome),name="uhome"),
    path('profile/delete/<slug:slug>',login_required(views.delete_user),name="delete_user"),
    path('logout',login_required(views.tlogout),name='logout'),
    path('files/delete/<slug:slug>',login_required(views.file_delete),name='file_delete'),
    #path('tfiles/update/<slug:>slug',login_required(views.allfiles),name='upfile'),
    path('files',login_required(views.allfiles),name='upfile'),
    path('notifications',login_required(views.t_notification_home),name='logout'),
    path('notifications/<slug:slug>',login_required(views.t_notification_handle),name='t_notification_handle'),
    path('notifications/delete/<slug:slug>',login_required(views.t_notification_delete),name='t_notification_delete'),
    path('tup_file',login_required(views.tup_file),name='tup_file'),
    path('profile',login_required(views.profile),name='profile'),
    path('profile/<slug:slug>',login_required(views.view_profile_t),name='view_profile_t'),
    path('upload_pic',login_required(views.upload_pic_t),name='uplaod_pic_t'),
]