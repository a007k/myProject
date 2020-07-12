from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path('login',views.ulog,name="home"),
    path('resend',login_required(views.u_resend_otp),name="home"),
    path('otpverify',login_required(views.uotpverify),name="home"),
    path('home',login_required(views.uhome),name="home"),
    path('logout',login_required(views.ulogout),name='logout'),
    path('trequest',login_required(views.trequest),name='trequest'),
    path('arequest',login_required(views.arequest),name='arequest'),
    path('trequest/<slug:slug>',login_required(views.send_frequest_t),name='frequest'),
    path('arequest/<slug:slug>',login_required(views.send_frequest_a),name='frequest'),
    path('trequest/delete/<slug:slug>',login_required(views.frequest_delete_t),name='frequest_delete'),
    path('arequest/delete/<slug:slug>',login_required(views.frequest_delete_a),name='frequest_delete'),
    path('files',login_required(views.user_file),name='ufile'),
    path('profile',login_required(views.profile),name='profile'),
    path('upload_pic',login_required(views.upload_pic_u),name='uplaod_pic_u'),
    path('key_submit/<slug:slug>',login_required(views.s_key_check),name='s_key'),
    
]

