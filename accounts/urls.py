from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('emaillogin/', views.email_login, name='email_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.UserPageView.as_view(), name='profile'),
    path('', views.UserLibraryView.as_view(), name='dashboard'),
]
