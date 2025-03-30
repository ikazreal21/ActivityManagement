from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.contrib.auth.models import Group
from admin_interface.models import Theme


admin.site.unregister(Group)
# admin.site.unregister(Theme)
# admin.site.register()
admin.site.register(EventPlace)
admin.site.register(Reservation)
admin.site.register(Profile)



admin.site.site_title = "Activity Management Admin"
admin.site.site_header = "Activity Management Admin"
