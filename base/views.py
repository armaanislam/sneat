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
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(username=username)

        except:
            messages.warning(request, 'User does not exists.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, 'Successfully logged in!')
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'The username or password is incorrect.')

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
            user = User.objects.filter(username__iexact=username)
            if user.exists():
                messages.warning(request, 'Username already exists')
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
    lists = User.objects.all()

    context = {'lists': lists}
    return render(request, 'base/account-tables.html', context)



@login_required(login_url='auth-login-basic')
def accountAdd(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            validate_email(email)
            user = User.objects.filter(username__iexact=username)
            if user.exists():
                messages.warning(request, 'Username already exists')
            else:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                address = request.POST.get('address')
                phone_number = request.POST.get('phone_number')
                organization = request.POST.get('organization')
                state = request.POST.get('state')
                zipcode = request.POST.get('zipcode')

                user = User.objects.create(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    address = address,
                    phone_number = phone_number,
                    organization = organization,
                    state = state,
                    zipcode = zipcode,
                )
                user.save()
                messages.success(request, 'Account added successfully!')
                return redirect('account-tables')
        except ValidationError:
            messages.warning(request, 'Enter a valid email')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/account-add.html', context)



@login_required(login_url='auth-login-basic')
def accountEdit(request, pk):
    user = User.objects.get(id=pk)
    form = MyUserCreationForm(instance=user)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            validate_email(email)
            if user.username == username:
                user.email = email
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.address = request.POST.get('address')
                user.phone_number = request.POST.get('phone_number')
                user.organization = request.POST.get('organization')
                user.state = request.POST.get('state')
                user.zipcode = request.POST.get('zipcode')
                user.save()
                messages.success(request, 'Account edited successfully!')
                return redirect('account-tables')
            else:
                user = User.objects.filter(username=username)
                if user.exists():
                    messages.warning(request, 'Username already exists')
                else:
                    user.username = username
                    user.email = email
                    user.first_name = request.POST.get('first_name')
                    user.last_name = request.POST.get('last_name')
                    user.address = request.POST.get('address')
                    user.phone_number = request.POST.get('phone_number')
                    user.organization = request.POST.get('organization')
                    user.state = request.POST.get('state')
                    user.zipcode = request.POST.get('zipcode')
                    user.save()
                    messages.success(request, 'Account edited successfully!')
                    return redirect('account-tables')

        except ValidationError:
            messages.warning(request, 'Enter a valid email')

    else:
        messages.error(request, '')

    context = {'form': form, 'user': user}
    return render(request, 'base/account-edit.html', context)



@login_required(login_url='auth-login-basic')
def accountDelete(request, pk):
    user = User.objects.get(id=pk)
    form = MyUserCreationForm(instance=user)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('account-tables')
    context = {'object': user, 'form': form}
    return render(request, 'base/account-delete.html', context)



@login_required(login_url='auth-login-basic')
def accountChangePassword(request, pk):
    user = User.objects.get(id=pk)
    form = MyUserCreationForm(instance=user)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('account-tables')
    context = {'object': user, 'form': form}
    return render(request, 'base/account-change-password.html', context)
