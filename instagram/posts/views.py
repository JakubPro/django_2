from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

@login_required
def home(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'posts/homeSite.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        if image:
            Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('homeSite')
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
