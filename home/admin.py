from django.contrib import admin

# Register your models here.
from .models import OurTeam
from .models import Contect_admin

admin.site.register(OurTeam)
admin.site.register(Contect_admin)

