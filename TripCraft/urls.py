# urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# Add page paths here (Atheen)
urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_app/', include('admin_app.urls')),
    path('user_app/', include('user_app.urls')),
]
