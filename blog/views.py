from django.shortcuts import render, redirect
from blog.models import User, Blog, Comment
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
# Create your views here.



def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and first_name and last_name and email and password:
            if not User.objects.filter(Q(username=username) | Q(email=email)).exists():
                User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Username or email already exists.')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'register.html')

@login_required(login_url='login')
def home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    items_per_page = 5
    paginator = Paginator(blogs, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'home.html', context={'data': blogs, 'page': page})

@login_required(login_url='login')
def show_data(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        comment_text = request.POST.get('comment')
        email = request.POST.get('email')
        if comment_text:
            user = request.user
            if user.is_authenticated:
                  Comment.objects.create(blog=blog, user=user, text=comment_text)
            else:
                pass
        if email:
            subject = 'Check out this blog post!'
            message = f'Hi there! Check out this blog post: {request.build_absolute_uri(blog.get_absolute_url())}'
            sender_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            # Send the email
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
    return render(request, 'show_data.html', {'blog': blog})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})


def logout(request):
    auth_logout(request)
    return redirect('login')




