from django.shortcuts import render,redirect
from .models import OurTeam
from .models import Contect_admin
from django.contrib import messages
# Create your views here.
def home(request):
    ourteams = OurTeam.objects.all()
    return render(request,"index.html",{'ourteams':ourteams})

def xhome(request):
    ourteams = OurTeam.objects.all()
    return render(request,"table.html",{'ourteams':ourteams})    

def msg_to_admin(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']

        if (len(first_name)==0):
            messages.info(request,'Your First name is empty')
            return redirect('/')
        elif (len(last_name)==0):
            messages.info(request,'Your Last name is empty')
            return redirect('/')
        elif (len(email)==0):
            messages.info(request,'Put your email')
            return redirect('/')
        elif (len(subject)==0):
            messages.info(request,'Subject is Empty')
            return redirect('/')
        elif (len(message)==0):
            messages.info(request,'Message is empty')
            return redirect('/')
        else:
            admin_msg=Contect_admin.objects.create(first_name=first_name,last_name=last_name,email=email,subject=subject,message=message)
            admin_msg.save()
            return render(request,"index.html")

   # return render(request,"index.html")

''' ourteam1=OurTeam()
    ourteam1.name='Ankit'
    ourteam1.post='developer'
    ourteam1.img='person_1.jpg'
    ourteam1.f='https://www.youtube.com/'

    ourteam2=OurTeam()
    ourteam2.name='Ankit'
    ourteam2.post='developer'
    ourteam2.img='person_2.jpg'
    ourteam1.f='https://www.youtube.com/'

    ourteam3=OurTeam()
    ourteam3.name='Ankit'
    ourteam3.post='developer'
    ourteam3.img='person_3.jpg'
    ourteam1.f='https://www.youtube.com/'
    ourteams=[ourteam1,ourteam2,ourteam3]
    #ourteams = OurTeam.objects.all()

    return render(request,"index.html",{'ourteams':ourteams})'''