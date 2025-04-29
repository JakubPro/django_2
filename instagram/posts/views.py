from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Dozwolone tylko pliki JPG, JPEG, PNG lub GIF')

def home(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'posts/homeSite.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        
        try:
            if image:
                validate_image_extension(image)
                post = Post.objects.create(user=request.user, image=image, caption=caption)
                return redirect('homeSite')
            else:
                raise ValidationError('Musisz wybrać zdjęcie')
        except ValidationError as e:
            return render(request, 'posts/postSite.html', {'error': str(e)})
    
    return render(request, 'posts/postSite.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homeSite')
    else:
        form = UserCreationForm()
    return render(request, 'posts/signupSite.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homeSite')
    else:
        form = AuthenticationForm()
    return render(request, 'posts/loginSite.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homeSite')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'posts/profileSite.html', {'profile_user': user, 'posts': posts})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))