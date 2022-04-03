from django import forms

from .models import Album


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
