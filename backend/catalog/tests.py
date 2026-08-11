from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Album, Artist, Song


class CatalogApiTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Massive Attack")
        self.album = Album.objects.create(title="Mezzanine", artist=self.artist, release_year=1998)

    def test_album_contains_ordered_tracks(self):
        angel = Song.objects.create(title="Angel")
        teardrop = Song.objects.create(title="Teardrop")
        self.client.post(reverse("album-add-track", args=[self.album.pk]), {"song_id": teardrop.pk, "track_number": 3})
        self.client.post(reverse("album-add-track", args=[self.album.pk]), {"song_id": angel.pk, "track_number": 1})
        response = self.client.get(reverse("album-detail", args=[self.album.pk]))
        self.assertEqual([track["track_number"] for track in response.data["tracks"]], [1, 3])

    def test_same_song_can_have_different_number_in_another_album(self):
        song = Song.objects.create(title="Angel")
        other = Album.objects.create(title="Collected", artist=self.artist, release_year=2006)
        self.assertEqual(self.client.post(reverse("album-add-track", args=[self.album.pk]), {"song_id": song.pk, "track_number": 1}).status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.post(reverse("album-add-track", args=[other.pk]), {"song_id": song.pk, "track_number": 7}).status_code, status.HTTP_201_CREATED)

    def test_duplicate_track_number_is_rejected(self):
        self.client.post(reverse("album-add-track", args=[self.album.pk]), {"song_title": "Angel", "track_number": 1})
        response = self.client.post(reverse("album-add-track", args=[self.album.pk]), {"song_title": "Teardrop", "track_number": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_future_release_year_is_rejected(self):
        response = self.client.post(reverse("album-list"), {"title": "Future", "artist": self.artist.pk, "release_year": date.today().year + 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_finds_song(self):
        self.client.post(reverse("album-add-track", args=[self.album.pk]), {"song_title": "Teardrop", "track_number": 3})
        response = self.client.get(reverse("album-list"), {"search": "tear"})
        self.assertEqual(len(response.data), 1)

