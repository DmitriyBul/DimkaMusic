import random
from itertools import chain
from random import choice

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import ListView, View
import json

from taggit.models import Tag

from accounts.forms import UserRegistrationForm
from accounts.models import Profile
from music.forms import SearchForm, PlaylistForm, AddToPlaylistForm
from .models import Album, Song, UserLibrarylist, Artist, UsersAlbumRating, UserPlaylist, PlayList


class HomeView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        albums = Album.objects.all()[:6]
        template_name = 'music/home.html'
        form = UserRegistrationForm()
        context = {'albums': albums, 'form': form}
        return render(request, template_name, context)

    def post(self, request, ordering='AZ', *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})


class AlbumDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        album = get_object_or_404(Album, id=self.kwargs['id'], slug=self.kwargs['slug'])
        number = self.kwargs['nia']
        song = Song.objects.get(album=album, number_in_album=number)
        number = self.kwargs['nia'] + 1
        songs_count = Song.objects.filter(album__id=album.id).count()
        playlist_form = AddToPlaylistForm()

        in_favourites = False
        if request.user.is_authenticated:
            UsersAlbumRating.objects.get_or_create(user=request.user, album=album, rating=0)
            rating = \
                list(UsersAlbumRating.objects.filter(user=request.user, album=album).values_list('rating', flat=True))[
                    0]

            playlist_form.fields['users_playlists'].queryset = PlayList.objects.filter(userplaylist__user=request.user)
            try:
                UserLibrarylist.objects.get(user=request.user, album=album)
                in_favourites = True
            except:
                in_favourites = False
        else:
            rating = album.rating
        album_tags = list(album.tags.all())

        random_albums = random.sample(album_tags, len(album_tags))

        recommended_albums = Album.objects.filter(tags__in=random_albums).exclude(name=album.name)
        template_name = 'music/album_detail.html'
        context = {'album': album, 'song': song, 'rating': rating, 'songs_count': songs_count, 'number': number,
                   'playlist_form': playlist_form, 'in_favourites': in_favourites, 'recommended_albums': recommended_albums}
        return render(request, template_name, context)

    def post(self, request, ordering='AZ', *args, **kwargs):
        playlist_form = AddToPlaylistForm(request.POST)
        if playlist_form.is_valid():
            return redirect("/home/")


@login_required
def add_album_to_library(request, id):
    album = get_object_or_404(Album, id=id)
    UserLibrarylist.objects.get_or_create(user=request.user, album=album)
    return redirect('accounts:dashboard')


class NewAlbumsListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        albums = Album.objects.order_by('-created')[:12]
        lst = Paginator(albums, 12)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'music/new_albums.html'
        context = {'page_obj': page_obj}
        return render(request, template_name, context)


class ArtistsListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        artists = Artist.objects.order_by('name')
        lst = Paginator(artists, 12)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'music/artists.html'
        context = {'page_obj': page_obj}
        return render(request, template_name, context)


class ArtistDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        artist = get_object_or_404(Artist, id=self.kwargs['id'], slug=self.kwargs['slug'])
        albums = Album.objects.filter(artist=artist).order_by('year')
        lst = Paginator(albums, 12)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'music/artist_detail.html'
        context = {'page_obj': page_obj, 'artist': artist}
        return render(request, template_name, context)


class AlbumsListView(ListView):
    def get(self, request, ordering='AZ', tag_slug=None, *args, **kwargs):
        albums = Album.objects.order_by('name')
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            albums = albums.filter(tags__in=[tag])
        lst = Paginator(albums, 12)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'music/albums.html'
        context = {'page_obj': page_obj, 'tag': tag}
        return render(request, template_name, context)


class TagsListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        tags = Tag.objects.all()
        template_name = 'music/tags_list.html'
        context = {'tags': tags}
        return render(request, template_name, context)


class SearchResultsView(ListView):
    template_name = 'music/search.html'
    context_object_name = 'results'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        album_list = Album.objects.annotate(
            search=SearchVector('name', 'artist'),
        ).filter(search=query)
        artist_list = Artist.objects.annotate(
            search=SearchVector('name'),
        ).filter(search=query)
        queryset = {'album_list': album_list, 'artist_list':
            artist_list}
        return queryset


def rate_album(request, id, slug, nia):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        album = get_object_or_404(Album, id=id)
        UsersAlbumRating.objects.filter(user=request.user, album=album).update(rating=val)
        return HttpResponseRedirect(request.path_info)
    return HttpResponseRedirect(request.path_info)


class RandomSong(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        album_ids = Album.objects.values_list('id', flat=True)
        random_album_id = choice(album_ids)
        album = Album.objects.get(id=random_album_id)
        # ids = Song.objects.filter(album=album).values_list('id', flat=True)
        songs_ids = list(Song.objects.filter(album__name=album.name).values_list('id', flat=True))
        ids = random.choice(songs_ids)
        # random_id = choice(ids)
        song = Song.objects.get(id=ids)
        template_name = 'music/random_song.html'
        context = {'album': album, 'song': song}
        return render(request, template_name, context)


class PlaylistListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        playlist_ids = list(UserPlaylist.objects.filter(user=request.user).values_list('id', flat=True))
        playlists = PlayList.objects.filter(id__in=playlist_ids)
        lst = Paginator(playlists, 12)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'music/playlists.html'
        context = {'page_obj': page_obj}
        return render(request, template_name, context)


class PlaylistDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        playlist = get_object_or_404(PlayList, id=self.kwargs['id'])
        number = self.kwargs['nia']
        songs = playlist.songs.select_related('album').all()
        song = songs[number]
        songs_count = playlist.songs.count()
        template_name = 'music/playlist_detail.html'
        context = {'playlist': playlist, 'song': song, 'songs_count': songs_count, 'number': number}
        return render(request, template_name, context)


@login_required
def add_song_to_playlist(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        playlist_id = request.POST.get('p_id')
        end_index = playlist_id.index('&')
        print(playlist_id[16:end_index])
        playlist_id = int(playlist_id[16:end_index])
        song = get_object_or_404(Song, id=id)
        playlist = get_object_or_404(PlayList, id=playlist_id)
        playlist.songs.add(song)
        return HttpResponseRedirect(request.path_info)
    return HttpResponseRedirect(request.path_info)


@login_required
def delete_song_from_playlist(request, id, p_id):
    song = get_object_or_404(Song, id=id)
    playlist = get_object_or_404(PlayList, id=p_id)
    if playlist.songs.count() == 0:
        return redirect('music:my_playlists')
    else:
        playlist.songs.remove(song)
        return redirect('music:playlist_detail', id=p_id, nia=0)


class CreatePlaylist(View, LoginRequiredMixin):
    model = PlayList
    form_class = PlaylistForm
    template_name = 'music/playlist_create.html'
    success_url = reverse_lazy('music:user_playlists')


@login_required
def delete_album_from_library(request, id):
    album = get_object_or_404(Album, id=id)
    record = UserLibrarylist.objects.get(user=request.user, album=album)
    record.delete()
    return redirect('accounts:dashboard')
