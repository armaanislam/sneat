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
from .forms import *
from .models import *
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



@login_required(login_url='auth-login-basic')
def employeeTables(request):
    lists = Employee.objects.all()

    context = {'lists': lists}
    return render(request, 'base/employee-tables.html', context)



@login_required(login_url='auth-login-basic')
def kpiConfig(request):
    lists = KPIConfig.objects.all()

    context = {'lists': lists}
    return render(request, 'base/kpi-configuration-tables.html', context)



@login_required(login_url='auth-login-basic')
def project(request):
    lists = Project.objects.all()

    context = {'lists': lists}
    return render(request, 'base/project-tables.html', context)



@login_required(login_url='auth-login-basic')
def reviewRating(request):
    lists = ReviewRating.objects.all()

    context = {'lists': lists}
    return render(request, 'base/review-rating-tables.html', context)



@login_required(login_url='auth-login-basic')
def sbu(request):
    lists = SBU.objects.all()

    context = {'lists': lists}
    return render(request, 'base/sbu-tables.html', context)



@login_required(login_url='auth-login-basic')
def subSBU(request):
    lists = SubSBU.objects.all()

    context = {'lists': lists}
    return render(request, 'base/sub-sbu-tables.html', context)



@login_required(login_url='auth-login-basic')
def supervisor(request):
    lists = Supervisor.objects.all()

    context = {'lists': lists}
    return render(request, 'base/supervisor-tables.html', context)



@login_required(login_url='auth-login-basic')
def kpiObjective(request):
    lists = KPIObjective.objects.all()

    context = {'lists': lists}
    return render(request, 'base/kpi-objective-tables.html', context)



@login_required(login_url='auth-login-basic')
def employeeAdd(request):

    form = EmployeeForm()

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.filter(employee_id=employee_id) #.get = error?
        if employee.exists():
            messages.error(request, 'Employee already exists!')
            return redirect('employee-add')
        else:
            name = request.POST.get('name')
            designation = request.POST.get('designation')
            sbu = request.POST.get('sbu')
            sub_sbu = request.POST.get('sub_sbu')
            basic_salary = request.POST.get('basic_salary')
            supervisor = request.POST.get('supervisor')
            project = request.POST.get('project')

            employee = Employee.objects.create(
                name = name,
                employee_id = employee_id,
                designation = designation,
                sbu = SBU.objects.get(id=sbu),
                sub_sbu = SubSBU.objects.get(id=sub_sbu),
                basic_salary = basic_salary,
                supervisor = Supervisor.objects.get(id=supervisor),
                project = Project.objects.get(id=project),
                created_by = request.user,
                updated_by = request.user
            )
            employee.save()
            messages.success(request, 'New employee added!')
            return redirect('employee-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/employee-add.html', context)



@login_required(login_url='auth-login-basic')
def kpiConfigAdd(request):

    form = KpiConfigForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        shortlist = request.POST.get('shortlist')
        kpiconfig = KPIConfig.objects.filter(shortlist=shortlist)

        if kpiconfig.exists():
            messages.error(request, 'Duplicate entry for shortlist')
            return redirect('kpi-config-add')

        else:
            kpiconfig = KPIConfig.objects.create(
                name = name,
                shortlist = shortlist,
                created_by = request.user,
                updated_by=request.user,
            )
            kpiconfig.save()
            messages.success(request, 'New configuration added!')
            return redirect('kpi-config-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/kpi-configuration-add.html', context)



@login_required(login_url='auth-login-basic')
def reviewRatingAdd(request):

    form = ReviewRatingForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        rating = request.POST.get('rating')
        reviewrating = ReviewRating.objects.filter(rating=rating)

        if reviewrating.exists():
            messages.error(request, 'Duplicate entry for rating')
            return redirect('review-rating-add')

        else:
            reviewrating = ReviewRating.objects.create(
                name = name,
                rating = rating,
                created_by = request.user,
                updated_by=request.user,
            )
            reviewrating.save()
            messages.success(request, 'New rating added!')
            return redirect('review-rating-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/review-rating-add.html', context)



@login_required(login_url='auth-login-basic')
def supervisorAdd(request):

    form = SupervisorForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        supervisor = Supervisor.objects.create(
            name = name,
            created_by=request.user,
            updated_by=request.user,
        )
        supervisor.save()
        messages.success(request, 'New supervisor added!')
        return redirect('supervisor-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/supervisor-add.html', context)



@login_required(login_url='auth-login-basic')
def projectAdd(request):

    form = ProjectForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        project = Project.objects.create(
            name = name,
            created_by=request.user,
            updated_by=request.user,
        )
        project.save()
        messages.success(request, 'New project added!')
        return redirect('project-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/project-add.html', context)


@login_required(login_url='auth-login-basic')
def sbuAdd(request):

    form = SBUForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        sbu = SBU.objects.create(
            name = name,
            created_by=request.user,
            updated_by=request.user,
        )
        sbu.save()
        messages.success(request, 'New SBU added!')
        return redirect('sbu-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/sbu-add.html', context)



@login_required(login_url='auth-login-basic')
def subSbuAdd(request):

    form = SubSBUForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        subsbu = SubSBU.objects.create(
            name = name,
            created_by=request.user,
            updated_by=request.user,
        )
        subsbu.save()
        messages.success(request, 'New Sub SBU added!')
        return redirect('sub-sbu-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/sub-sbu-add.html', context)



@login_required(login_url='auth-login-basic')
def kpiObjectiveAdd(request):

    form = KpiObjectiveForm()

    if request.method == 'POST':

        name = request.POST.get('name')
        kpiobjective = KPIObjective.objects.create(
            name = name,
            created_by=request.user,
            updated_by=request.user,
        )
        kpiobjective.save()
        messages.success(request, 'New KPI Objective added!')
        return redirect('kpi-objective-tables')

    else:
        messages.error(request, '')

    context = {'form': form}
    return render(request, 'base/kpi-objective-add.html', context)