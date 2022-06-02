from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import UserForm, MyUserCreationForm
from .models import User


def registerPage(request):
    user = User.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            validate_email(email)
            password = request.POST.get('password')
            user = User.objects.filter(Q(username=username) | Q(email=email))
            if user.exists():
                messages.warning(request, 'Username or email already exists')
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success(request, 'Account created successfully!')
                login(request, user)
                return redirect('index')

        except ValidationError:
            messages.warning(request, 'Enter a valid email')

    else:
        messages.error(request, '')
    context = {}
    return render(request, 'base/auth-register-basic.html', context)


def loginUser(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(email=email)

        except:
            messages.warning(request, 'User does not exists.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            messages.success(request, 'Successfully logged in!')
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'The email or password is incorrect.')

    return render(request, 'base/auth-login-basic.html')


def logoutUser(request):
    logout(request)
    return redirect('auth-login-basic')


def forgotPassword(request):

    context = {}
    return render(request, 'base/auth-forgot-password-basic.html', context)


@login_required(login_url='auth-login-basic')
def indexPage(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'base/index.html', context)


@login_required(login_url='auth-login-basic')
def accountTables(request):

    context = {}
    return render(request, 'base/account-tables.html', context)


@login_required(login_url='auth-login-basic')
def accountAdd(request):
    context = {}
    return render(request, 'base/account-add.html', context)



