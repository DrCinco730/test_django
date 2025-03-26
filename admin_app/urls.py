from django.urls import path
from . import views

# URL routes here 
urlpatterns = [
    path('analytics/', views.analytics, name='analytics'),
    path('monitor/', views.monitor, name='monitor'),
]