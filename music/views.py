from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.views.generic import ListView, View
import json

from accounts.forms import UserRegistrationForm
from accounts.models import Profile
from .models import Album, Song, UserLibrarylist


class HomeView(ListView):
    def get(self, request, category_slug=None, ordering='AZ', *args, **kwargs):
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
        songs = Song.objects.filter(album=album).order_by('number_in_album')
        template_name = 'music/album_detail.html'
        context = {'album': album, 'songs': songs}
        return render(request, template_name, context)


@login_required
def add_album_to_library(request, id):
    album = get_object_or_404(Album, id=id)
    UserLibrarylist.objects.get_or_create(user=request.user, album=album)
    return redirect("/home/")


class NewAlbumsListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        albums = Album.objects.order_by('-created')[:12]
        lst = Paginator(albums, 6)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'music/new_albums.html'
        context = {'page_obj': page_obj}
        return render(request, template_name, context)
