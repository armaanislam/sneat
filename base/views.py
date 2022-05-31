from django.shortcuts import render, redirect
#from django.contrib import messages
#from django.db.models import Q
#from django.http import HttpResponse
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
#from .models import *
#from .forms import *

def loginUser(request):

    check = 'login'
    context = {'check': check}
    return render(request, 'base/auth-login-basic.html', context)
