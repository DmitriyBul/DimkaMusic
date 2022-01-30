from django.db import models

# Create your models here.
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='music/artist', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'artist'
        verbose_name_plural = 'artists'

    def __str__(self):
        return self.name

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

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:album_detail', args=[self.id, self.slug])


class Song(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    file = models.FileField(upload_to='music/song')
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
