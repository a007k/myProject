from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from tlog_app.models import CustomUser
from django.contrib import messages

from django.http import HttpResponse
# Create your views here.
def reg(request):
    if request.method=='POST':
        #Name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        Fname=request.POST['fname']
        Lname=request.POST['lname']

        if password==password1:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'user taken')
                #print('user taken')
                return redirect('/user/register')
            elif CustomUser.objects.filter(email=email):
                #print('email taken')
                messages.info(request,'email taken')
                return redirect('/user/register')

            else:
                user=CustomUser.objects.create_user(username=username,email=email,password=password,first_name=Fname,last_name=Lname)
                user.save()
                return redirect('/user/login')
                #print("user created")
        else:
            #print("pasword not matching")
            messages.info(request,'password not matching')
            return redirect('/user/register')

        
        return redirect('/')
    
    else:
        return render(request,"ureg.html")