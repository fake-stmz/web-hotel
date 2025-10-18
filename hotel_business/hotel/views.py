from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Service

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        print("User not authenticated, redirecting to login page")
        return redirect('login')

    services = Service.objects.all()
    context = { 'services': services }

    return render(request, 'index.html', context)


def login_page(request):
    
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=login_input, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль.'})
    
    return render(request, 'login.html')

def register_page(request):

    if request.method == 'POST':
        login_input = request.POST.get('login')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')

        if password == password_confirm:
            user = User.objects.create_user(username=login_input, first_name=first_name, last_name=last_name, email=email, password=password)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'error': 'Пароли не совпадают.'})

    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('login')