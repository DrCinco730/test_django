from django.urls import path
from django.views.generic import TemplateView

from . import views


# URL routes here
urlpatterns = [
    path('analytics/', views.analytics, name='analytics'),
    # path('monitor/', views.monitor, name='monitor'),
    # # User management actions
    # path('edit-user/', views.edit_user, name='edit_user'),
    # path('reset-password/', views.reset_user_password, name='reset_user_password'),
    # path('toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    # path('delete-user/', views.delete_user, name='delete_user'),

    # path('dashboard', TemplateView.as_view(template_name='0dashboard.html'), name='admin_dashboard'),
    # path('base', TemplateView.as_view(template_name='base_admin.html'), name='base'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('poi/', views.poi_list, name='poi_list'),
    path('poi/create/', views.poi_create, name='poi_create'),
    path('poi/<int:pk>/edit/', views.poi_edit, name='poi_edit'),
    path('dashboard/', views.category_list, name='dashboard'),

    path('travelers/', views.traveler_list, name='traveler_list'),
    path('travelers/<int:pk>/', views.traveler_detail, name='traveler_detail'),
    path('support/', views.support_ticket_list, name='support_ticket_list'),
    path('support/<int:pk>/', views.support_ticket_detail, name='support_ticket_detail'),

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),

    # Admin notification routes
    path('user/notifications/', views.notification_list, name='notification_list'),
    path('user/notifications/create/', views.notification_create, name='notification_create'),
    path('user/notifications/<int:pk>/delete/', views.notification_delete, name='notification_delete'),

    # User notification routes
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),

]