"""astrology URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', views.backend_dashboard_login, name='backendlogin'),
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('birthdata/', views.birthdata, name='birthdata'),
    path('readingrate/', views.readingrate, name='readingrate'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    path('changepass/', views.user_change_pass, name='changepass'),
    
    
    path('backend-login/', views.backend_dashboard_login, name='backendlogin'),
    path('backend-login/backend/', views.backend_dashboard, name='backend'),
    path('backend-login/backend/viewdetail/<int:id>', views.viewdetail_dashboard, name='viewdetail'),
    path('backend-login/backend/deletedetail/<int:id>', views.deletedetail_dashboard, name='deletedetail'),
    path('backend/view-birth-details/<int:id>', views.view_birth_details, name='view-birth-details'),
    path('backend/send-mail-single-birth/<int:id>', views.send_mail_single_birth, name='send-mail-single-birth'),
    path('backend/send-mail-multiple-birth/<int:user_id>', views.send_mail_multiple_birth, name='send-mail-multiple-birth'),

    # path('backend-login/backend/complete_viewdetail/<int:id>', views.complete_viewdetail_dashboard, name='complete_viewdetail'),
    path('backend_dashboard_logout/', views.backend_dashboard_logout, name='backend_dashboard_logout'),
    path('backend_dashboard_changpassword/', views.backend_dashboard_changpassword, name='backend_dashboard_changpassword'),
       
]
