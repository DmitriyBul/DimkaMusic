from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.views.generic import ListView, View
import json
from .models import Album, Song


class HomeView(ListView):
    def get(self, request, category_slug=None, ordering='AZ', *args, **kwargs):
        albums = Album.objects.all()[:6]
        template_name = 'music/home.html'
        context = {'albums': albums}
        return render(request, template_name, context)


class AlbumDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        album = get_object_or_404(Album, id=self.kwargs['id'], slug=self.kwargs['slug'])
        songs = Song.objects.filter(album=album).order_by('number_in_album')
        template_name = 'music/album_detail.html'
        context = {'album': album, 'songs': songs}
        return render(request, template_name, context)
