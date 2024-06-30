from django.contrib import admin
from .models import PoliceStation, Complain, Attachment


admin.site.register(PoliceStation)
admin.site.register(Attachment)
admin.site.register(Complain)