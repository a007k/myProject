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

def key_generator(size=10, chars=string.ascii_letters + string.digits + string.punctuation):
    global x
    x=''.join(random.choice(chars) for _ in range(size))
    return x


# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password,is_admin=True)  
        if user is not None:
            if user.is_authority==True:
                otp=id_generator()    
                send_mail( 'Your OTP',
                otp,
                'filetransferkey@gmail.com',
                [user.email],
                fail_silently=False)
                auth.login(request,user)
                return redirect('/authority/otpverify')
            else:
                messages.info(request,'you are not a trustee')
                return redirect('/authority/login')

            
        else:
            messages.info(request,'invalid credentials')
            return redirect('/authority/login')
    else:
        if request.user.is_authenticated:
            return redirect('/user/home')
        else:
            return render(request,"tlog.html")


#to send otp

def resend_otp(request):
    otp=id_generator()    
    send_mail( 'Your OTP',otp,'filetransferkey@gmail.com',[request.user.email],fail_silently=False)
    auth.login(request,request.user)
    messages.info(request,'OTP has been sent')
    return redirect('/authority/otpverify')


def otpverify(request):
    if request.method=='POST':
        value=request.POST['key']
        if(value==x):
            return redirect('/authority/home')
        else:
            messages.info(request,'wrong OTP')
            return redirect('/authority/otpverify')
    else:
        return render(request,"otp.html")




#home view
from tlog_app.models import CustomUser
def home(request):
    print(request.user.password)
    users=CustomUser.objects.filter(is_admin=False)
    requests=Request.objects.filter(astatus="Pending")
    context={"users":users,"requests":requests}
    return render(request,"thome.html",context)


#for deleting the file from home
def delete_user(request,slug,val=0):
    instance = CustomUser.objects.get(id=slug)
    if instance.is_authority and val==0:
        #print("you cant't delete trustee")
        messages.info(request,"you cant't delete an Authority")
        return redirect('view_profile_a',slug=instance.id)
    else:
        instance.delete()
        return redirect('/authority/home')



def logout(request):
    auth.logout(request)
    return redirect('/')

#for uploadin files of thome
from tlog_app.models import Files

from decimal import *
def allfiles(request):
    if request.method=='POST':
        name=request.POST['name']
        file1=request.FILES['img_logo']
        file_size=request.FILES['img_logo'].size
        file_size=file_size/(1024*1024)
        file_name=request.FILES['img_logo'].name
        format=request.FILES['img_logo'].content_type
        fileobj=Files.objects.create(name=name,files=file1,file_size=file_size,file_name=file_name,format=format)
        fileobj.save()
        return redirect('/authority/files')
    else:
        files=Files.objects.all()
        requests=Request.objects.filter(astatus="Pending")
        context={"files":files,"requests":requests}
        return render(request,"tfile.html",context)
#to delete any file
def file_delete(request,slug):
    instance = Files.objects.get(id=slug)
    instance.delete()
    return redirect('/authority/files')


def t_resend_otp(request):
    otp=id_generator()    
    send_mail( 'Your OTP',
    otp,
    'filetransferkey@gmail.com',
    [request.user.email],
    fail_silently=False)
    auth.login(request,request.user)
    messages.info(request,'OTP has been sent')
    return redirect('/authority/otpverify')


def totpverify(request):
    if request.method=='POST':
        value=request.POST['key']
        if(value==x):
            return redirect('/authority/home')
        else:
            messages.info(request,'wrong OTP')
            return redirect('/authority/otpverify')
    else:
        return render(request,"otp.html")
#for geting the request in notification
from ulog_app.models import Request
def t_notification_home(request):
    requests=Request.objects.filter(astatus="Pending")
    request1=Request.objects.filter(astatus="Pending")
    request2=Request.objects.filter(astatus="Accesed")
    requestall=request1|request2
    context={"requests":requests,"requestall":requestall,"val":1}
    return render(request,'tnotifications.html',context)

#for posting the request in notification
from ulog_app.models import Request
def t_notification_handle(request,slug):
    #print("asdjskj")
    files=Request.objects.get(id=slug)
    if files.astatus=="Pending":
        files.astatus="Accesed"
        otp=key_generator()    
        send_mail( 'Your Key is ',
        "FILE NAME ->  "+ str(files.files.name)+ " \n KEY ->  " + otp,
        'filetransferkey@gmail.com',[request.user.email],
        fail_silently=False)
        files.s_key=otp
        #auth.login(request,request.user)
    elif files.astatus=="Accesed":
        files.s_key="a"
        files.dnld="False"
        files.astatus="Pending"
    files.save()
    return redirect('/authority/notifications')

#for checking only
def tup_file(request):
    return render(request,'changepassword.html')


#for deleting the notifications
def t_notification_delete(request,slug):
    instance = Request.objects.get(id=slug)
    instance.astatus="Not sent"
    instance.s_key="a"
    #instance.delete()
    instance.save()
    return redirect('/authority/notifications')

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
            return redirect('/authority/profile')
         
        if(email==current_user.email):
            pass
        elif CustomUser.objects.filter(email=email):
            #print("allredy exist")
            messages.info(request,'email taken')
            return redirect('/authority/profile')
        if check_password(password,current_user.password):
            pass
        else:
            messages.info(request,'Wrong current password')
            return redirect('/authority/profile')

            
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        about=request.POST['about']
        current_user.email=email
        current_user.username=username
        current_user.first_name=first_name
        current_user.last_name=last_name
        current_user.about=about
        current_user.save()
        return redirect('/authority/profile')

#to change image

def upload_pic_a(request):
    if request.method == 'POST':
        image=request.FILES['file']
        user=request.user
        user.image=image
        user.save()
    return redirect('/authority/profile')


def view_profile_a(request,slug):
    user=CustomUser.objects.get(id=slug)
    context={"user":user}
    return render(request,"view_profile.html",context) 

