from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from .models import User
from .forms import UserForm, MyUserCreationForm

@login_required(login_url='auth-login-basic')
def indexPage(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'base/index.html', context)


def loginUser(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email-username')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(email=email, password=password)
        except:
            messages.error(request, 'User does not exists!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            messages.success(request, 'Successfully logged in!')
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email or password do not exist!')

    context = {}
    return render(request, 'base/auth-login-basic.html', context)


def logoutUser(request):
    logout(request)
    return redirect('auth-login-basic')


def registerPage(request):
    user = User.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, '')
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, '')
    context = {}
    return render(request, 'base/auth-register-basic.html', context)



def forgotPassword(request):

    context = {}
    return render(request, 'base/auth-forgot-password-basic.html', context)


