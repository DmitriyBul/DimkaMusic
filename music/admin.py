from django.contrib import admin

# Register your models here.
from .forms import AlbumForm
from .models import Artist, Album, Song, UserLibrarylist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'year', 'artist', 'created']
    list_filter = ['name', 'year', 'artist']
    list_editable = ['year', 'artist']
    prepopulated_fields = {'slug': ('name',)}
    add_form_template = 'music/admin/album_form.html'
    change_form_template = 'admin/album_form.html'

    def get_form(self, form_class=None, obj=None, **kwargs):
        try:
            instance = kwargs['instance']
            return AlbumForm(instance=instance)
        except KeyError:
            return AlbumForm

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = self.get_form(request)
        return super(AlbumAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        album = Album.objects.get(id=object_id)
        extra_context["form"] = self.get_form(instance=album)
        return super(AlbumAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.save()
        songs = request.FILES.getlist('songs')
        i = 1
        for song in songs:
            index = song.name.rfind('.')
            name = song.name[:index]
            Song.objects.create(album=obj, name=name, file=song, number_in_album=i)
            i += 1
        return super().save_model(request, obj, form, change)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'album', 'number_in_album']
    list_filter = ['name', 'album']
    list_editable = ['number_in_album', 'album']


@admin.register(UserLibrarylist)
class UserLibrarylistAdmin(admin.ModelAdmin):
    list_display = ['user', 'album']
    list_filter = ['user', 'album']
    list_editable = ['album']
