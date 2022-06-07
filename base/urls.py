from django.urls import path
from . import views

urlpatterns = [

    #Index page
    path('index/', views.indexPage, name='index'),

    #Register, Login, Logout, ForgotPassword
    path('auth-register-basic/', views.registerPage, name='auth-register-basic'),
    path('', views.loginUser, name='auth-login-basic'),
    path('logout/', views.logoutUser, name='logout'),
    path('auth-forgot-password/', views.forgotPassword, name='auth-forgot-password'),

    #Account-Table, Account Change Password, Account-CRUD operation
    path('account-tables/', views.accountTables, name='account-tables'),
    path('account-add/', views.accountAdd, name='account-add'),
    path('account-change-password/<str:pk>/', views.accountChangePassword, name='account-change-password'),
    path('account-edit/<str:pk>/', views.accountEdit, name='account-edit'),
    path('account-delete/<str:pk>/', views.accountDelete, name='account-delete'),

]
