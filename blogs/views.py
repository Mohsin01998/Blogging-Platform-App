from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Profile
import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required

def send_mail_after_registration(email, token):
    subject='Your accounts need to be verified'
    message=f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            try:
                user = form.save(commit=False)
                user.save()
                auth_token=str(uuid.uuid4())
                profile_obj=Profile.objects.create(user=user,email_token=auth_token)
                profile_obj.save()
                send_mail_after_registration(email,auth_token)
                return redirect('token')
            except Exception as e:
                print(e)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def verify(request, auth_token):
    try:
        profile_obj=Profile.objects.filter(email_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,'Your account has been verified. ')
            return redirect('success')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, 'Username not found.')
                return redirect('login')

            profile_obj = Profile.objects.filter(user=user_obj).first()
            if not profile_obj.is_verified:
                messages.error(request, 'Your profile is not verified. Check your email.')
                return redirect('login')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Wrong username or password.')
                return redirect('login')

            # Check if user is active, if not activate the user
            if not user.is_active:
                user.is_active = True
                user.save()

            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def error(request):
    return render(request,'error.html')
def token(request):
    return render(request,'account_activation_email.html')
def success(request):
    return render(request,'verification_complete.html')
@login_required
def home(request):
    return render(request,'index.html')
def about_us(request):
    return render(request,'about_us.html')

def blogs(request):
    return render(request,'blogs.html')

def contact_us(request):
    return render(request,'contact_us.html')

def logout_view(request):
    logout(request)
    return redirect('/')
