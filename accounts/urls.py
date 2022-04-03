from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.UserPageView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('emaillogin/', views.email_login, name='email_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.UserLibraryView.as_view(), name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

