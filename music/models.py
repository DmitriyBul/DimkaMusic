from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from taggit.managers import TaggableManager
# Create your models here.
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField


class Artist(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='artists/', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'artist'
        verbose_name_plural = 'artists'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:artist_detail', args=[self.id, self.slug])
    # def get_absolute_url(self):
    # return reverse('products:product_list_by_category', args=[self.slug])


class Album(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    year = models.IntegerField(blank=True)
    image = models.ImageField(upload_to='albums/', blank=True)
    artist = models.ForeignKey(Artist,
                               related_name='albums',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:album_detail', args=[self.id, self.slug])


class Song(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    file = models.FileField(upload_to='music/song', blank=True)
    album = models.ForeignKey(Album,
                              related_name='songs',
                              on_delete=models.CASCADE)
    number_in_album = models.IntegerField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'song'
        verbose_name_plural = 'songs'

    def __str__(self):
        return self.name


class UserLibrarylist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30, null=True, blank=True)


# Doesn't work
# class AlbumRatingByUser(models.Model):
    # album = models.ForeignKey(Album, on_delete=models.CASCADE)
    # ratings = ArrayField(models.IntegerField(default=0, blank=True,
                                             # validators=[MaxValueValidator(5),
                                                         # MinValueValidator(0)]), blank=True)
    # users = ArrayField(models.CharField(max_length=200, blank=True), blank=True)


class UsersAlbumRating(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, blank=True)
