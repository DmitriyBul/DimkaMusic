from django import forms
from django.http import request

from .models import Album, PlayList


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['songs'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                               required=False)

    class Meta:
        model = Album
        fields = '__all__'


class SearchForm(forms.Form):
    query = forms.CharField()


class PlaylistForm(forms.ModelForm):
    name = forms.CharField(label='Name of the playlist', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter a name of the playlist'
    }))
    image = forms.ImageField(
        label='Playlist image', widget=forms.FileInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = PlayList
        fields = 'name', 'image'

'''
class AddToPlaylistForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddToPlaylistForm, self).__init__(*args, **kwargs)

        users_playlists = forms.ModelChoiceField(
            label='Add to ', queryset=PlayList.objects.filter(user=request.user), widget=forms.Select(
                attrs={'class': 'form-control js-example-basic-single'}
            )
        )
'''
