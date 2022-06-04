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
    path('random/', views.RandomSong.as_view(), name='random_song'),
    path('artists/', views.ArtistsListView.as_view(), name='artists'),
    path('albums/', views.AlbumsListView.as_view(), name='albums'),

    path('playlists/add/', views.add_song_to_playlist, name='add_to_playlist'),
    path('playlists/delete/<int:id>/<int:p_id>/', views.delete_song_from_playlist, name='delete_from_playlist'),
    path('playlists/', views.PlaylistListView.as_view(), name='my_playlists'),
    path('playlists/<int:id>/<int:nia>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),

    path('<int:id>/<slug:slug>/<int:nia>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('<int:id>/<slug:slug>/<int:nia>/rate_album/', views.rate_album, name='rate_album'),

    path('music/<int:id>/add/', views.add_album_to_library, name='add_album'),
    path('artists/<int:id>/<slug:slug>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('new_albums/', views.NewAlbumsListView.as_view(), name='new_albums'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('tag/<slug:tag_slug>/', views.AlbumsListView.as_view(), name='albums_by_tag'),
    path('genres/', views.TagsListView.as_view(), name='tags_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
