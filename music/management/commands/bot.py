from datetime import timedelta
from threading import Thread
from time import sleep

import schedule
import telebot
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from telebot import types
from django.core.management.base import BaseCommand
from django.conf import settings

from accounts.models import TelegramUserRelation
from music.models import Album, Artist, UserLibrarylist
import re


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),
                  s)


def save_telegram_user(username, password, telegram_user_id):
    username = username.replace(' ', '')
    password = password.replace(' ', '')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            TelegramUserRelation.objects.get_or_create(user=user, telegram_id=telegram_user_id)
            return True
        else:
            return False
    except:
        return False


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

        def schedule_checker():
            while True:
                schedule.run_pending()
                sleep(1)

        def news_sender():
            day = timezone.now().date() - timedelta(days=7)
            albums = Album.objects.filter(created__gte=day)
            for i in range(len(albums)):
                users_ids = list(UserLibrarylist.objects.filter(album__artist=albums[i].artist).values_list('user__username', flat=True))
                print(users_ids)
                telegram_ids = list(TelegramUserRelation.objects.filter(user__username__in=users_ids).values_list('telegram_id', flat=True))
                print(telegram_ids)
                for id in telegram_ids:
                    text = f'Добавлен новый альбом группы {albums[i].artist} - {albums[i].name}'
                    bot.send_message(id, text)
                    bot.send_photo(id, albums[i].image)

            return


        @bot.message_handler(commands=["start"])
        def start(m, res=False):
            bot.send_message(m.chat.id,
                             'Привет! Это информационный бот для DimkaMusic Web App. Что тебя интересует? =)')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура
            key_albums = types.KeyboardButton(text='Альбомы')
            key_artists = types.KeyboardButton(text='Исполнители')
            key_register = types.KeyboardButton(text='Подписаться')
            keyboard.add(key_albums, key_artists, key_register)  # добавляем кнопку в клавиатуру
            bot.send_message(m.chat.id,
                             'Выбери интересующее: ',
                             reply_markup=keyboard)

        @bot.message_handler(content_types=["text"])
        def handle_text(message):
            global album_search
            global artist_search
            global authorizing

            if message.text.strip() == 'Альбомы':
                answer = "Альбомы"
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура
                key_albums_news = types.KeyboardButton(text='Новые альбомы')
                key_albums_search = types.KeyboardButton(text='Поиск альбомов')
                key_back = types.KeyboardButton(text='Назад')
                keyboard.add(key_albums_news, key_albums_search, key_back)  # добавляем кнопку в клавиатуру
                bot.send_message(message.chat.id,
                                 'Выбери, что тебя интересует из этого раздела:',
                                 reply_markup=keyboard)

            elif message.text.strip() == 'Новые альбомы':
                answer = "Новые альбомы"
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура

                key_back = types.KeyboardButton(text='Назад')
                keyboard.add(key_back)  # добавляем кнопку в клавиатуру
                albums = list(Album.objects.all().order_by('-created').values_list('name', flat=True))[:5]
                artists = list(Album.objects.all().order_by('-created').values_list('artist__name', flat=True))[:5]

                text = ''
                for i in range(len(albums)):
                    text += f'{i + 1}. {artists[i]} - {albums[i]} \n'
                bot.send_message(message.chat.id,
                                 text,
                                 reply_markup=keyboard)

            elif message.text.strip() == 'Поиск альбомов':
                answer = "Напиши, какой альбом ищешь?"
                album_search = True
                bot.send_message(message.chat.id,
                                 'Альбомы')

            elif message.text.strip() == 'Подписаться':

                answer = "Напиши свой логин и пароль через запятую. Например: 'username, password'"
                album_search = False
                artist_search = False
                authorizing = True
                bot.send_message(message.chat.id,
                                 'Подписка на рассылку')

            elif message.text.strip() == 'Исполнители':
                answer = "Исполнители"
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура
                key_artists_news = types.KeyboardButton(text='Новые исполнители')
                key_artists_search = types.KeyboardButton(text='Поиск исполнителей')
                key_back = types.KeyboardButton(text='Назад')
                keyboard.add(key_artists_news, key_artists_search, key_back)  # добавляем кнопку в клавиатуру

                bot.send_message(message.chat.id,
                                 'Выбери, что тебя интересует из этого раздела:',
                                 reply_markup=keyboard)

            elif message.text.strip() == 'Новые исполнители':
                answer = "Новые исполнители"
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура

                key_back = types.KeyboardButton(text='Назад')
                keyboard.add(key_back)  # добавляем кнопку в клавиатуру
                artists = list(Artist.objects.all().order_by('-created').values_list('name', flat=True))[:5]
                text = ''
                for i in range(len(artists)):
                    text += f'{i + 1}. {artists[i]} \n'
                bot.send_message(message.chat.id,
                                 text,
                                 reply_markup=keyboard)
            elif message.text.strip() == 'Поиск исполнителей':
                answer = "Напиши, какого исполнителя ищешь?"
                artist_search = True
                album_search = False
                bot.send_message(message.chat.id,
                                 'Исполнители')
            elif message.text.strip() == 'Назад':
                answer = 'Что тебя интересует? =)'
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура
                key_albums = types.KeyboardButton(text='Альбомы')
                key_artists = types.KeyboardButton(text='Исполнители')
                key_register = types.KeyboardButton(text='Подписаться')
                keyboard.add(key_albums, key_artists, key_register)  # добавляем кнопку в клавиатуру
                bot.send_message(message.chat.id,
                                 'Выбери интересующее: ',
                                 reply_markup=keyboard)
            else:
                if album_search:
                    artist_search = False

                    bot.send_message(message.chat.id,
                                     f'Ищем альбом {message.text}')
                    search_word = str(message.text)

                    text = ''
                    try:
                        album = get_object_or_404(Album, name=titlecase(search_word))

                        text += 'Нашел! \n'
                        text += '*************\n'
                        text += f'Название - {album.name}\n Исполнитель - {album.artist}\n Год - {str(album.year)}\n'
                        text += '*************\n'
                        text += f'http://127.0.0.1:8000{album.get_absolute_url()}\n'

                        bot.send_message(message.chat.id,
                                         text)
                        bot.send_photo(message.chat.id, album.image)

                    except:
                        bot.send_message(message.chat.id,
                                         f'Ничего не найдено. Попробуй снова =(')
                    answer = f'Поиск завершен'
                    album_search = False
                elif artist_search:
                    bot.send_message(message.chat.id,
                                     f'Ищем исполнителя {message.text}')

                    search_word = str(message.text)

                    text = ''
                    try:
                        artist = get_object_or_404(Artist, name=titlecase(search_word))
                        albums_count = Album.objects.filter(artist=artist).count()

                        text += 'Нашел! \n'
                        text += '*************\n'
                        text += f'Исполнитель - {artist.name}\n Количество альбомов на DimkaMusic - {albums_count}\n'
                        text += '*************\n'

                        bot.send_message(message.chat.id,
                                         text)
                        bot.send_photo(message.chat.id, artist.image)

                    except:
                        bot.send_message(message.chat.id,
                                         f'Ничего не найдено. Попробуй снова =(')

                    answer = f'Поиск завершен'
                    artist_search = False

                elif authorizing:
                    try:
                        username = str(message.text).split(',')[0]
                        password = str(message.text).split(',')[1]
                        is_success = save_telegram_user(username, password, str(message.chat.id))

                        if is_success:
                            answer = f'Пользователь сохранен'
                        else:
                            answer = f'Не удалось найти пользователя. Попробуйте снова'
                    except:
                        answer = "Что-то пошло не так. Попробуйте снова"
                else:
                    answer = "Что-то пошло не так. Попробуйте снова"

            schedule.every().week.do(news_sender)
            Thread(target=schedule_checker).start()
            bot.send_message(message.chat.id, answer)

        bot.polling(none_stop=True, interval=0)
