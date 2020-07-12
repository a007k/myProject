from django.db import models

# Create your models here.
from tlog_app.models import CustomUser,Files

Status_Val=(
    ("Not Sent","Not Sent"),
    ("Pending","Pending"),
    ("Accesed","Accesed"),
      
)

D_Status_Val=(
    ("False","False"),
    ("True","True"),
  
)

from django.utils import timezone
class Request(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    files=models.ForeignKey(Files,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
    tstatus=models.CharField(max_length=30,choices=Status_Val,default="Not Sent")
    update_on = models.DateTimeField(auto_now_add=False,auto_now=True)
    Access_time= models.DateTimeField(default=timezone.now)
    astatus=models.CharField(max_length=30,choices=Status_Val,default="Not sent")
    s_key=models.CharField(blank=True,max_length=20,default="a")
    dnld=models.CharField(max_length=5,choices=D_Status_Val,default="False")