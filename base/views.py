from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from .forms import MyUserCreationForm
from .models import User
from .helpers import send_forgot_password_mail
import uuid



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



def changePassword(request, token):

    try:
        user = User.objects.filter(forget_password_token=token).first()
        print(user)
    except Exception as e:
        print(e)

    context = {'user_id': user.id}
    return render(request, 'base/change-password.html', context)



def forgotPassword(request):

    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            user = User.objects.get(username=username)

            if user:
                user = User.objects.get(username=username)
                token = str(uuid.uuid4())
                user.forget_password_token = token
                user.save()
                mail = send_forgot_password_mail(user.email, token)
                print(mail)
                messages.success(request, 'An email has been sent!')
                print('test2')
                return redirect('auth-forgot-password')

            else:
                print('test1')
                messages.error(request, 'No username found with this username')
                return redirect('auth-forgot-password')



    except Exception as e:
        print(e)

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
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        try:
            validate_email(email)
            user = User.objects.filter(username__iexact=username)
            if user.exists():
                messages.warning(request, 'Username already exists')
            elif password != password_confirmation:
                messages.error(request, 'Passwords do not match')
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
                user.set_password(password_confirmation)
                user.save()
                update_session_auth_hash(request, user)
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
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        try:
            validate_email(email)
            if user.username == username:
                if password != password_confirmation:
                    messages.error(request, 'Passwords do not match')
                else:
                    user.email = email
                    user.set_password(password_confirmation)
                    user.first_name = request.POST.get('first_name')
                    user.last_name = request.POST.get('last_name')
                    user.address = request.POST.get('address')
                    user.phone_number = request.POST.get('phone_number')
                    user.organization = request.POST.get('organization')
                    user.state = request.POST.get('state')
                    user.zipcode = request.POST.get('zipcode')
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Account edited successfully!')
                    return redirect('account-tables')
            else:
                user = User.objects.filter(username=username)
                if user.exists():
                    messages.warning(request, 'Username already exists')
                elif password != password_confirmation:
                    messages.error(request, 'Passwords do not match')
                else:
                    user.username = username
                    user.email = email
                    user.set_password(password_confirmation)
                    user.first_name = request.POST.get('first_name')
                    user.last_name = request.POST.get('last_name')
                    user.address = request.POST.get('address')
                    user.phone_number = request.POST.get('phone_number')
                    user.organization = request.POST.get('organization')
                    user.state = request.POST.get('state')
                    user.zipcode = request.POST.get('zipcode')
                    user.save()
                    update_session_auth_hash(request, user)
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
    current_password = user.password

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        matchcheck =  check_password(old_password, current_password)

        if matchcheck != True:
            messages.error(request, 'Old password incorrect')
        elif new_password1 != new_password2:
            messages.error(request, 'Passwords do not match')
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('account-tables')
    context = {'user': user}
    return render(request, 'base/account-change-password.html', context)



@login_required(login_url='auth-login-basic')
def accountChangePasswordAdmin(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match')
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('account-tables')
    context = {'user': user}
    return render(request, 'base/account-change-password-admin.html', context)