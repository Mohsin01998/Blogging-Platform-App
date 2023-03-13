from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .forms import RegisterForm, CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Profile, Post, Category
import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url='login')
def add_comment(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


@login_required(login_url='login')
def post_delete(request,post_id):
    # Retrieve the post object with the specified ID
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request,'post_delete.html')
@login_required(login_url='login')
def post_edit(request,post_id):
    # Retrieve the post object with the specified ID
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
         # Retrieve the updated post data from the form
        title = request.POST.get('title')
        body = request.POST.get('body')
        category_name = request.POST.get('category')

        # Check if the category already exists in the database
        category, created = Category.objects.get_or_create(name=category_name)

        # Update the post's fields with the new values
        post.title = title
        post.body = body
        post.category = category
        date = datetime.datetime.now()
        post.date=date

        # Save the updated post to the database
        post.save()
        return redirect('home')

    # Render the edit post page with the current post data
    return render(request, 'post_edit.html', {'post': post})
@login_required(login_url='login')
def post_create(request):
    if request.method=='POST':
        title=request.POST.get('title')
        body=request.POST.get('body')
        category_name = request.POST.get('category')
        # Check if the category already exists in the database
        category, created = Category.objects.get_or_create(name=category_name)
        author=request.user
        date=datetime.datetime.now()
        post=Post.objects.create(title=title,body=body,category=category,author=author,date=date)
        post.save()
        return redirect('home')
    return render(request,'post_creation.html')
@login_required(login_url='login')
def home(request):
    user_id=request.user.id
    post_form=Post.objects.filter(author=user_id)
    return render(request, 'index.html',{'post_form':post_form})

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

def about_us(request):
    return render(request,'about_us.html')


def contact_us(request):
    return render(request,'contact_us.html')

def logout_view(request):
    logout(request)
    return redirect('/')
