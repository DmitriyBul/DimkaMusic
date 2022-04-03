from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    path('', lambda req: redirect('/home/')),
    path('home/', views.HomeView.as_view(), name='home'),
    path('artists/', views.ArtistsListView.as_view(), name='artists'),
    path('albums/', views.AlbumsListView.as_view(), name='albums'),
    path('<int:id>/<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('music/<int:id>/add/', views.add_album_to_library, name='add_album'),
    path('artists/<int:id>/<slug:slug>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('new_albums/', views.NewAlbumsListView.as_view(), name='new_albums'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('tag/<slug:tag_slug>/', views.AlbumsListView.as_view(), name='albums_by_tag')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
