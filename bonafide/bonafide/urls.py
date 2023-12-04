"""
URL configuration for bonafide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from bonafide_management import views 
from apis.views import *
# from .views import student_registration
from bonafide_management.views import student_registration, STUDENTSUCCESSVIEW, signup, login, bonafide_details, admin_login, admin_home, STUDENTDETAILSVIEW, base_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "",
        TemplateView.as_view(template_name="base.html"),
        name="base",
    ),
    path('bonafide_details/', bonafide_details, name='bonafide_details'),
    path('student-registration/', views.student_registration, name='student_registration'),
    path('admin_login/',admin_login,name='admin_login'),
    path("student-success/", STUDENTSUCCESSVIEW.as_view(), name="student_success"),
    
    path('admin_home/',admin_home, name='admin_home'),
    # path('bonafide_details/', bonafide_details, name='bonafide_details'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    # path('base/', base_view, name='base'),
    path('verify_login_otp/', views.verify_login_otp, name='verify_login_otp'),
    # path('', lambda request: redirect('base'), name='home_redirect'),
    
]