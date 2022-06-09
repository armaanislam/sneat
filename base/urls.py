from django.urls import path
# from django.auth import views as auth_views
from . import views

urlpatterns = [

    #Index page
    path('index/', views.indexPage, name='index'),

    #Register, Login, Logout, ForgotPassword, ChangePassword
    path('auth-register-basic/', views.registerPage, name='auth-register-basic'),
    path('', views.loginUser, name='auth-login-basic'),
    path('logout/', views.logoutUser, name='logout'),
    path('auth-forgot-password/', views.forgotPassword, name='auth-forgot-password'),
    # path('change-password/', auth_views.PasswordResetView.as_view())
    path('change-password/<token>/', views.changePassword, name='change-password'),

    #Account-Table, Account Change Password, Account-CRUD operation
    path('account-tables/', views.accountTables, name='account-tables'),
    path('account-add/', views.accountAdd, name='account-add'),
    path('account-change-password/<str:pk>/', views.accountChangePassword, name='account-change-password'),
    path('account-change-password-admin/<str:pk>/', views.accountChangePasswordAdmin, name='account-change-password-admin'),
    path('account-edit/<str:pk>/', views.accountEdit, name='account-edit'),
    path('account-delete/<str:pk>/', views.accountDelete, name='account-delete'),

    #Employee-Table
    path('employee-tables/', views.employeeTables, name='employee-tables'),

    #KPI-Configuration
    path('kpi-config/', views.kpiConfig, name='kpi-config'),

    #Review Rating, SBU, subSBU, Supervisor, Project, KpiObjective
    path('review-rating/', views.reviewRating, name='review-rating'),
    path('sbu/', views.sbu, name='sbu'),
    path('sub-sbu/', views.subSBU, name='sub-sbu'),
    path('project/', views.project, name='project'),
    path('supervisor/', views.supervisor, name='supervisor'),
    path('kpi-objective/', views.kpiObjective, name='kpi-objective'),

]
