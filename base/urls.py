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
    path('change-password/<token>/', views.changePassword, name='change-password'),


    #Account-Table, Account Change Password, Account-CRUD operation
    path('account-tables/', views.accountTables, name='account-tables'),
    path('account-add/', views.accountAdd, name='account-add'),
    path('account-change-password/<str:pk>/', views.accountChangePassword, name='account-change-password'),
    path('account-change-password-admin/<str:pk>/', views.accountChangePasswordAdmin, name='account-change-password-admin'),
    path('account-edit/<str:pk>/', views.accountEdit, name='account-edit'),
    path('account-delete/<str:pk>/', views.accountDelete, name='account-delete'),


    #Employee, KPI-Configuration, Review Rating, SBU, subSBU, Supervisor, Project, KpiObjective TABLES
    path('employee-tables/', views.employeeTables, name='employee-tables'),
    path('kpi-config-tables/', views.kpiConfig, name='kpi-config-tables'),
    path('review-rating-tables/', views.reviewRating, name='review-rating-tables'),
    path('sbu-tables/', views.sbu, name='sbu-tables'),
    path('sub-sbu-tables/', views.subSBU, name='sub-sbu-tables'),
    path('project-tables/', views.project, name='project-tables'),
    path('supervisor-tables/', views.supervisor, name='supervisor-tables'),
    path('kpi-objective-tables/', views.kpiObjective, name='kpi-objective-tables'),


    #Employee, KPI-Configuration, Review Rating, SBU, subSBU, Supervisor, Project, KpiObjective tables ADD
    path('employee-add/', views.employeeAdd, name='employee-add'),
    path('kpi-config-add/', views.kpiConfigAdd, name='kpi-config-add'),
    path('review-rating-add/', views.reviewRatingAdd, name='review-rating-add'),
    path('supervisor-add/', views.supervisorAdd, name='supervisor-add'),

]
