from django import forms

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
