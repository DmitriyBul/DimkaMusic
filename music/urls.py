from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    path('', lambda req: redirect('/home/')),
    path('home/', views.HomeView.as_view(), name='album_list'),
    path('<int:id>/<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('music/<int:id>/add/', views.add_album_to_library, name='add_album'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
