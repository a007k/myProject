from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from tlog_app.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
from django.core.mail import send_mail

import random
import string
#x="ankit"
def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    global x
    x=''.join(random.choice(chars) for _ in range(size))
    return x 


# Create your views here.
def tlog(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password,is_admin=True)  
        if user is not None:
            if user.is_trustee==True:
                otp=id_generator()    
                send_mail( 'Your OTP',
                otp,
                'filetransferkey@gmail.com',
                [user.email],
                fail_silently=False)
                auth.login(request,user)
                return redirect('/trustee/otpverify')
            else:
                messages.info(request,'you are not a trustee')
                return redirect('/trustee/login')

            
        else:
            messages.info(request,'invalid credentials')
            return redirect('/trustee/login')
    else:
        if request.user.is_authenticated:
            return redirect('/user/home')
        else:
            return render(request,"tlog.html")


# Create your views here.

from .models import CustomUser
def thome(request):
    print(request.user.password)
    users=CustomUser.objects.filter(is_admin = False).filter(is_authority=False)
    requests=Request.objects.filter(tstatus="Pending")
    context={"users":users,"requests":requests}
    return render(request,"thome.html",context)
#for deleting the file from home
def delete_user(request,slug):
    instance = CustomUser.objects.get(id=slug)
    if instance.is_trustee:
        print("you cant't delete a Trustee")
        messages.info(request,"you cant't delete a Trustee")
        return redirect('view_profile_t',slug=instance.id)
    else:
        print("sacnd")
        instance.delete()
        return redirect('/trustee/home')



def tlogout(request):
    auth.logout(request)
    return redirect('/')

#for uploadin files of thome
from .models import Files
from .models import Files
from decimal import *
def allfiles(request):
    if request.method=='POST':
        file1=request.FILES['img_logo']
        if not file1:
            messages.info(request,'No file chosen')
            return redirect('/trustee/files')
        name=request.POST['name']
        if not name:
            messages.info(request,'Name can not be empty')
            return redirect('/trustee/files')
        if not file1:
            messages.info(request,'No file chosen')
            return redirect('/trustee/files')
        check = request.POST.get('use_stages', 0)
        
        file_size=request.FILES['img_logo'].size
        file_size=file_size/(1024*1024)
        file_name=request.FILES['img_logo'].name
        format=request.FILES['img_logo'].content_type
        fileobj=Files.objects.create(name=name,files=file1,file_size=file_size,file_name=file_name,format=format,hide=check)
        fileobj.save()
        return redirect('/trustee/files')
    else:
        files=Files.objects.all()
        requests=Request.objects.filter(tstatus="Pending")
        context={"files":files,"requests":requests}
        return render(request,"tfile.html",context)
#to delete any file
def file_delete(request,slug):
    instance = Files.objects.get(id=slug)
    instance.delete()
    return redirect('/trustee/files')


def t_resend_otp(request):
    otp=id_generator()    
    send_mail( 'Your OTP',
    otp,
    'filetransferkey@gmail.com',
    [request.user.email],
    fail_silently=False)
    auth.login(request,request.user)
    messages.info(request,'OTP has been sent')
    return redirect('/trustee/otpverify')


def totpverify(request):
    if request.method=='POST':
        value=request.POST['key']
        if(value==x):
            return redirect('/trustee/home')
        else:
            messages.info(request,'wrong OTP')
            return redirect('/trustee/otpverify')
    else:
        return render(request,"otp.html")
#for geting the request in notification
from ulog_app.models import Request
def t_notification_home(request):
    requestall=Request.objects.all()
    requests=Request.objects.filter(tstatus="Pending")
    context={"requests":requests,"requestall":requestall,"val":0}
    return render(request,'tnotifications.html',context)

#for posting the request in notification
from ulog_app.models import Request
def t_notification_handle(request,slug):
    files=Request.objects.get(id=slug)
    if files.tstatus=="Pending":
        files.tstatus="Accesed"
    else:
        files.tstatus="Pending"
    files.save()
    return redirect('/trustee/notifications')

#for checking only
def tup_file(request):
    return render(request,'footer.html')


#for deleting the notifications
def t_notification_delete(request,slug):
    instance = Request.objects.get(id=slug)
    instance.delete()
    return redirect('/trustee/notifications')

#this is for profile
from django.contrib.auth.hashers import check_password
def profile(request):
    if request.method=="GET":
        user=request.user
        context={"user":user}
        return render(request,"profile.html",context)
    else:
        current_user=request.user
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if(username==current_user.username):
            pass
        elif CustomUser.objects.filter(username=username):
            #print("allredy exist")
            messages.info(request,'user taken')
            return redirect('/trustee/profile')
         
        if(email==current_user.email):
            pass
        elif CustomUser.objects.filter(email=email):
            #print("allredy exist")
            messages.info(request,'email taken')
            return redirect('/trustee/profile')
        if check_password(password,current_user.password):
            pass
        else:
            messages.info(request,'Wrong current password')
            return redirect('/trustee/profile')

            
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        about=request.POST['about']
        current_user.email=email
        current_user.username=username
        current_user.first_name=first_name
        current_user.last_name=last_name
        current_user.about=about
        current_user.save()
        return redirect('/trustee/profile')

#to change image
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import CustomUser

def upload_pic_t(request):
    if request.method == 'POST':
        image=request.FILES['file']
        user=request.user
        user.image=image
        user.save()
    return redirect('/trustee/profile')



def view_profile_t(request,slug):
    user=CustomUser.objects.get(id=slug)
    context={"user":user}
    return render(request,"view_profile.html",context) 

