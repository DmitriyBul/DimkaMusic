from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from music.models import Artist, Album


class MusicURLSTest(TestCase):
    def setUp(self):
        self.artist_1 = Artist.objects.create(name='Artist_1', slug='artist_1')
        self.album_1 = Album.objects.create(name='test_album_1', artist=self.artist_1, year=2000)
        self.user = User.objects.create(username='test_username')

    def test_home(self):
        resolver = resolve('/home/')
        self.assertEqual(resolver.view_name, 'music:home')

    def test_detail_album(self):
        url = reverse('music:album_detail', args=[self.album_1.id, self.album_1.slug, 1])
        # response = self.client.get(reverse('music:album_detail', args=[self.album_1.id, self.album_1.slug, 1]))
        self.assertEqual(url, '/1/test_album_1/1/')

    # def test_search(self):
        # url = reverse('music:search', args=[self.album_1.id, self.album_1.slug, 1])
