from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.indexPage, name='index'),
    path('', views.loginUser, name='auth-login-basic'),
    path('logout/', views.logoutUser, name='logout'),
    path('auth-register-basic/', views.registerPage, name='auth-register-basic'),
    path('auth-forgot-password/', views.forgotPassword, name='auth-forgot-password'),
]
