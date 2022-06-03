from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import MyUserCreationForm
from .models import User


def loginUser(request):

    form = MyUserCreationForm()

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

    context = {'form': form}

    return render(request, 'base/auth-login-basic.html', context)


def logoutUser(request):
    logout(request)
    return redirect('auth-login-basic')


def registerPage(request):
    user = User.objects.all()
    form = MyUserCreationForm()

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
    context = {'form': form}
    return render(request, 'base/auth-register-basic.html', context)


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
    accounts = User.objects.all()

    context = {}
    return render(request, 'base/account-tables.html', context)


@login_required(login_url='auth-login-basic')
def accountAdd(request):
    user = User.objects.all()
    form = MyUserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            validate_email(email)
            user = User.objects.filter(Q(username=username) | Q(email=email))
            if user.exists():
                messages.warning(request, 'Username or email already exists')
            else:
                first_name = request.POST.get('firstname')
                last_name = request.POST.get('lastname')
                address = request.POST.get('address')
                phone_number = request.POST.get('phone_number')
                organization = request.POST.get('organization')
                country = request.POST.get('country')
                state = request.POST.get('state')
                zipcode = request.POST.get('zipcode')
                language = request.POST.get('language')

                user = User.objects.create( #abstract user wont create anything if we dont validate email #create_user only takes 2-4 positional arguments, so using create()
                    username = username,
                    email = email,
                    address = address,
                    phone_number = phone_number,
                    organization = organization,
                    country = country,
                    state = state,
                    zipcode = zipcode,
                    language = language,
                )
                user.save()
                return redirect('account-tables')
        except ValidationError:
            messages.warning(request, 'Enter a valid email')

    else:
        messages.error(request, 'An error has occured.')

    context = {'form': form, 'user': user}
    return render(request, 'base/account-add.html', context)



