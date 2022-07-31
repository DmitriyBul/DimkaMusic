import telebot
from telebot import types
from django.core.management.base import BaseCommand
from django.conf import settings

from music.models import Album


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

        @bot.message_handler(commands=["start"])
        def start(m, res=False):
            bot.send_message(m.chat.id,
                             'Привет! Это информационный бот для DimkaMusic Web App. Что тебя интересует? =)')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура
            key_albums = types.KeyboardButton(text='Альбомы')
            key_artists = types.KeyboardButton(text='Исполнители')
            keyboard.add(key_albums, key_artists)  # добавляем кнопку в клавиатуру
            bot.send_message(m.chat.id,
                             'Выбери интересующее: ',
                             reply_markup=keyboard)

        @bot.message_handler(content_types=["text"])
        def handle_text(message):
            global album_search
            global artist_search
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
                bot.send_message(message.chat.id,
                                 'Новые исполнители, которые были добавлены',
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
                keyboard.add(key_albums, key_artists)  # добавляем кнопку в клавиатуру
                bot.send_message(message.chat.id,
                                 'Выбери интересующее: ',
                                 reply_markup=keyboard)
            else:
                if album_search:
                    bot.send_message(message.chat.id,
                                     f'Ищем альбом {message.text}')
                    answer = f'Поиск завершен'
                    album_search = False
                elif artist_search:
                    bot.send_message(message.chat.id,
                                     f'Ищем исполнителя {message.text}')
                    answer = f'Поиск завершен'
                    artist_search = False
                else:
                    answer = "Что-то пошло не так. Попробуйте снова"

            bot.send_message(message.chat.id, answer)

        bot.polling(none_stop=True, interval=0)
