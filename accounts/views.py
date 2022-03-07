from music.models import Album, UserLibrarylist
from .models import Profile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.base import View

from .forms import LoginForm, UserRegistrationForm, EmailLoginForm
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
            albums = Album.objects.filter(name__in=user_album)
            # albums = Album.objects.filter(user=request.user).order_by('name')
            template_name = 'account/user_page.html'
            context = {'albums': albums}
            return render(request, template_name, context)
        else:
            return redirect('login/')


class UserPageView(View, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        user = request.user
        template_name = 'account/profile_card.html'
        context = {'user': user}
        return render(request, template_name, context)
