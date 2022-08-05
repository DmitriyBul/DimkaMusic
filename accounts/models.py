from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class TelegramUserRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=20, blank=True)
