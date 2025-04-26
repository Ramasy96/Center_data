from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from employees import views as emp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='employees/login.html'), name='login'),
        path('logout/', emp_views.logout_view, name='logout'),
    path('', include('employees.urls')),
]