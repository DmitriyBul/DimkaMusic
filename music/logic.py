from django.db.models import Avg
from django.http import request

from music.models import UsersAlbumRating


def set_rating(album, val=0):
    if 0 < int(val) <= 5:
        UsersAlbumRating.objects.filter(user=request.user, album=album).update(rating=val)
        rating = UsersAlbumRating.objects.filter(album=album).filter(rating__gt=0).aggregate(rating=Avg('rating')).get(
            'rating')
        album.rating = rating
        album.save()
