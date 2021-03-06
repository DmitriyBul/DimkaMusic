from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label=u'Username', help_text=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Username', help_text=False)
    password = forms.CharField(widget=forms.PasswordInput)


class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(label='New image', required=False,
                             error_messages={'invalid': "Image files only"}, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ('photo',)
