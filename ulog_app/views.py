from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from tlog_app.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
from django.core.mail import send_mail

#afunction to generate otp or key
import random
import string
x="dsabd"
def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    global x
    x=''.join(random.choice(chars) for _ in range(size))
    #print(x)
    return x


# Create your views here.
def ulog(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            otp=id_generator()    
            send_mail( 'Your OTP',
            otp,
            'filetransferkey@gmail.com',
            [user.email],
            fail_silently=False)
            auth.login(request,user)
            return redirect('/user/otpverify')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/user/login')
    else:
        if request.user.is_authenticated:
            return redirect('/user/home')
        else:
            return render(request,"ulog.html")

def uhome(request):
    val1=Request.objects.filter(user=request.user).filter(tstatus="Accesed")
    val2=Request.objects.filter(user=request.user).filter(astatus="Accesed")
    val3=Request.objects.filter(user=request.user).filter(astatus="Pending")
    val=val1 or val2 or val3
    x=False
    if(val):
        x=True
    context={"x":x}
    return render(request,"uhome.html",context)


def u_resend_otp(request):
    otp=id_generator()    
    send_mail( 'Your OTP',
    otp,
    'filetransferkey@gmail.com',
    [request.user.email],
    fail_silently=False)
    auth.login(request,request.user)
    messages.info(request,'OTP has been sent')
    return redirect('/user/otpverify')

def uotpverify(request):
    if request.method=='POST':
        value=request.POST['key']
        if(value==x):
            return redirect('/user/home')
        else:
            messages.info(request,'wrong OTP')
            return redirect('/user/otpverify')
    else:
        return render(request,"otp.html")

#this for request to trustee and file view
from tlog_app.models import Files
from .models import Request
def trequest(request):
        requests=Request.objects.filter(user=request.user)
        files=Files.objects.filter(hide=False)
        #print(requests)
        #obj=files&requests
        #print(obj)
        val1=Request.objects.filter(user=request.user).filter(tstatus="Accesed")
        val2=Request.objects.filter(user=request.user).filter(astatus="Accesed")
        val3=Request.objects.filter(user=request.user).filter(astatus="Pending")
        val=val1 or val2 or val3
        x=False
        if(val):
            x=True
        context={"files":files,"requests":requests,"x":x}
        
        return render(request,"ureq.html",context)

#this for request to authority and file view
def arequest(request):
        request1=Request.objects.filter(astatus="Pending")
        request2=Request.objects.filter(astatus="Accesed")
        requests=request1|request2
        files=Request.objects.filter(user=request.user).filter(tstatus="Accesed")
        
        #print(requests)
        #obj=files&requests
        #print(obj)
        x=True
        context={"files":files,"requests":requests,"x":x}
        
        return render(request,"areq.html",context)


#this to send request to the trustee in database
from .models import Request
from tlog_app.models import Files
def send_frequest_t(request,slug):
    files=Files.objects.get(id=int(slug))
    user=request.user
    if Request.objects.filter(user=user).filter(files=files):
        print("allready exist")
    else:
        Requestobj=Request.objects.create(files=files,user=user,tstatus="Pending",astatus="Not sent")
        Requestobj.save()
    return redirect('trequest')

# for sending the request to the authority
from .models import Request
from tlog_app.models import Files
def send_frequest_a(request,slug):
    #files=Files.objects.get(id=int(slug))
    user=request.user
    #if Request.objects.filter(user=user).filter(files=files):
    #    print("allready exist")
    #else:
    Requestobj=Request.objects.get(id=slug)
    Requestobj.astatus="Pending"
    Requestobj.save()
    #print(Requestobj.status)
    return redirect('arequest')
#for deleting the request by user
def frequest_delete_t(request,slug):
    instance = Request.objects.get(id=slug)
    instance.delete()
    return redirect('trequest')
def frequest_delete_a(request,slug):
    instance = Request.objects.get(id=slug)
    instance.astatus="Not Sent"
    instance.save()
    return redirect('arequest')

    
#to all the file which user can access
def user_file(request):
    user=request.user
    access=Request.objects.filter(user=user).filter(astatus="Accesed")
    val1=Request.objects.filter(user=request.user).filter(tstatus="Accesed")
    val2=Request.objects.filter(user=request.user).filter(astatus="Accesed")
    val3=Request.objects.filter(user=request.user).filter(astatus="Pending")
    val=val1 or val2 or val3
    x=False
    if(val):
        x=True
    context={"access":access,"x":x}
    return render(request,"ufiles.html",context)



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
            return redirect('/user/profile')
         
        if(email==current_user.email):
            pass
        elif CustomUser.objects.filter(email=email):
            #print("allredy exist")
            messages.info(request,'email taken')
            return redirect('/user/profile')
        if check_password(password,current_user.password):
            pass
        else:
            messages.info(request,'Wrong current password')
            return redirect('/user/profile')

            
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        about=request.POST['about']
        current_user.email=email
        current_user.username=username
        current_user.first_name=first_name
        current_user.last_name=last_name
        current_user.about=about
        current_user.save()

        print(username)
        print(email)
        return redirect('/user/profile')

def upload_pic_u(request):
    if request.method == 'POST':
        image=request.FILES['file']
        user=request.user
        user.image=image
        user.save()
    return redirect('/user/profile')



def ulogout(request):
    requests=Request.objects.filter(user=request.user).filter(astatus="Accesed")
    requests.astatus="Pending"
    requests.dnld="False"
    requests.delete()
    auth.logout(request)
    return redirect('/')



def s_key_check(request,slug):
    key=request.POST['key']
    req=Request.objects.get(id=slug)
    if str(req.s_key)==str(key):
        req.dnld="True"
        req.save()
        return redirect('/user/files')
    else:
        messages.info(request,"Wrong Secret Key")
        return redirect('/user/files')
    