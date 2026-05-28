from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import Profile
from apps.posts.models import Post
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! Ypu can now log in')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form  = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username = username)
    profile = get_object_or_404(Profile, user = user)
    posts = Post.published.filter(author = user).select_related('author')
    return render(request, 'user_profile.html', {
        'posts':posts,
        'profile': profile,
    })