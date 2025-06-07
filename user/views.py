from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .forms import CustomUserCreationForm
from .models import User, Student, Admin
from django.contrib.auth import logout


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            semester = form.cleaned_data.get('semester')
            if 'student_signup' in request.POST:
                user.is_student = True
                user.save()
                Student.objects.create(user=user, name=name, email=email, semester=semester)
            elif 'admin_signup' in request.POST:
                user.is_admin = True
                user.save()
                Admin.objects.create(user=user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_student:
                return redirect('homepage')
            elif user.is_admin:
                return redirect('homepage')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

def homepage_view(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            student = Student.objects.get(user=request.user)
            if student.application_status:
                context = {'show_buttons': True}
            else:
                context = {'show_buttons': False}
            return render(request, 'homepage.html', context)
        elif request.user.is_admin:
            #add admin homescreen here
            return redirect('login')
    else:
        return redirect('login')

