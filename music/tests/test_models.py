from django.contrib.auth.models import User
from django.test import TestCase

from music.models import Artist, Album, UsersAlbumRating, UserLibrarylist


class AlbumModelTest(TestCase):

    def setUp(self):
        self.artist_1 = Artist.objects.create(name='Artist_1', slug='artist_1')
        self.album_1 = Album.objects.create(name='test_album_1', artist=self.artist_1, year=2000)
        self.user = User.objects.create(username='test_username')

    def test_artist_create(self):
        test_artist = Artist.objects.get(name='Artist_1')
        field_label = test_artist._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        Artist.objects.create(name='Artist_2', slug='artist_2')
        artists_count = Artist.objects.count()
        self.assertEqual(2, artists_count)

    def test_album_create(self):
        test_album = Album.objects.get(name='test_album_1')
        self.assertEqual(test_album.name, 'test_album_1')


class AlbumRatingModelTest(TestCase):

    def setUp(self):
        self.artist_1 = Artist.objects.create(name='Artist_1', slug='artist_1')
        self.album_1 = Album.objects.create(name='test_album_1', artist=self.artist_1, year=2000)
        self.user = User.objects.create(username='test_username')
        self.user_2 = User.objects.create(username='test_username_2')

    def test_user_library(self):
        relation = UserLibrarylist.objects.create(album=self.album_1, user=self.user)
        count = UserLibrarylist.objects.count()
        self.assertEqual(1, count)
        UserLibrarylist.objects.create(album=self.album_1, user=self.user_2)
        count = UserLibrarylist.objects.count()
        self.assertEqual(2, count)
        relation.delete()
        count = UserLibrarylist.objects.count()
        self.assertEqual(1, count)
