from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    path('profile/', views.user_profile_view, name='user_profile'),
    path('update-profile/', views.user_profile_update, name='user_profile_update'),
]
