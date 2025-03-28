from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .utils import *

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localtime
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q

import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import Http404

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.dateparse import parse_date
from calendar import monthrange
from datetime import datetime, date, timedelta
from django.utils.timezone import make_aware

from django.contrib.auth.models import AnonymousUser

import pytz


# def LandingPage(request):
#     return render(request, 'activity/landing.html')


def Login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.info(request, "Username or Password is Incorrect")
    return render(request, 'activity/login.html')

def Register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            user_email = request.POST.get("email")
            if User.objects.filter(email=user_email).exists():
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass
                messages.error(request, "This email is already registered.")
                return redirect('login')
            
            form = CreateUserForm(request.POST)
            verification_code = create_rand_id()
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get("email")
                Profile.objects.create(
                    user=user,
                    email=email,
                    verification_code=verification_code
                )
                send_verification_email(email, user, verification_code)
            
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass


                messages.success(request, "Account Created For " + username)
                return redirect('login')
            else:
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass
                messages.info(request, "Make Sure your Credentials is Correct or Valid")
            
    context = {"form": form}
    return render(request, 'activity/login.html', context)

def Logout(request):
    logout(request)
    return redirect('login')

# Profile
def UserProfile(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        print(form)
        if form.is_valid():
            user_profile = form.save()
            user_profile.is_first_time = False
            user_profile.save()
            return redirect('user_profile')
    context = {'user_profile': user_profile}
    return render(request, 'activity/profile.html', context)

@login_required(login_url='login')
def Dashboard(request):
    return render(request, 'activity/dashboard.html')

# Calendar 
@login_required(login_url='login')
def calendar_view(request):
    return render(request, 'activity/calendar.html')

# Email Verification
def VerifyEmail(request, verification_code):
    patient = Profile.objects.get(verification_code=verification_code)
    patient.is_verified = True
    patient.save()
    return render(request, 'activity/verified.html')

def NeedVerification(request):
    logout(request)
    return render(request, 'activity/need_verification.html')

def send_verification_email(email, user, verification_code):
    subject = 'Email Verification'
    message = f'Hi {user.username},\n\nPlease click the link below to verify your email address:\n\nhttps://tctparking.ellequin.com/verify_email/{verification_code}'
    send_email(subject, message, [email])

    
def termsandconditions(request):
    return render(request, 'activity/termsandcondition.html')