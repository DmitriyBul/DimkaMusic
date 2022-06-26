from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

from accounts.models import Profile
from music.models import Album, UserLibrarylist, Song

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from django.views.generic.base import View

from .forms import UserRegistrationForm, EmailLoginForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


# create a function to resolve email to username
def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


# create a view that authenticate user with email
def email_login(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            username = get_user(email)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:home')
                else:
                    return redirect('music:home')
            else:
                return redirect('music:home')
    else:
        form = EmailLoginForm()
    return render(request, 'account/email_login.html', {'form': form})


class UserLibraryView(ListView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        if request.user.is_authenticated:
            user_album = list(UserLibrarylist.objects.filter(user=request.user).values_list('album__name', flat=True))
            print(user_album)
            albums = Album.objects.filter(name__in=user_album).order_by('name')
            lst = Paginator(albums, 12)
            page_number = request.GET.get('page')
            page_obj = lst.get_page(page_number)
            # albums = Album.objects.filter(user=request.user).order_by('name')
            template_name = 'account/user_page.html'
            context = {'page_obj': page_obj}
            return render(request, template_name, context)
        else:
            return redirect('login/')


class UserPageView(View, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        user = request.user
        total_albums = UserLibrarylist.objects.filter(user=request.user).count()
        album_ids = list(UserLibrarylist.objects.filter(user=request.user).values_list('album__id', flat=True))
        total_songs = Song.objects.filter(album__id__in=album_ids).count()
        template_name = 'account/profile_card.html'
        context = {'user': user, 'total_albums': total_albums, 'total_songs': total_songs}
        return render(request, template_name, context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile_update.html',
                          {'profile_form': profile_form})
'''
class ProfileEditView(UpdateView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        profile_form = ProfileEditForm(instance=profile)
        template_name = 'account/profile_update.html'
        context = {'form': profile_form}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():

            photo = profile_form.cleaned_data['photo']
            profile = Profile.objects.get(user=request.user)
            profile.photo = photo

            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']

            profile.save()
            Profile.objects.filter(user=request.user).update(photo=photo)
        return redirect('accounts:profile')
'''