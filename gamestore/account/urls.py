from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('authcheck/', views.is_user_logged_in),
    path('login/', auth_views.login, {'template_name': 'login2.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    path('change/', views.changeUser, name='changeuser'),
    path('register/', views.register_user, name='register'),
    path('verify/<str:token>/', views.verify, name='verify')
]
