from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower


def validate_release_year(value):
    if value < 1900 or value > date.today().year:
        raise ValidationError(f"Год должен быть между 1900 и {date.today().year}.")


class Artist(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(Lower("name"), name="artist_name_ci_unique")]

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=250)

    class Meta:
        ordering = ["title"]
        constraints = [models.UniqueConstraint(Lower("title"), name="song_title_ci_unique")]

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=250)
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)
    release_year = models.PositiveSmallIntegerField(validators=[validate_release_year])
    songs = models.ManyToManyField(Song, through="AlbumTrack", related_name="albums")

    class Meta:
        ordering = ["-release_year", "title"]
        constraints = [models.UniqueConstraint(Lower("title"), "artist", name="album_artist_title_ci_unique")]

    def __str__(self):
        return f"{self.artist} — {self.title}"


class AlbumTrack(models.Model):
    album = models.ForeignKey(Album, related_name="tracks", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name="track_entries", on_delete=models.CASCADE)
    track_number = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["track_number"]
        constraints = [
            models.UniqueConstraint(fields=["album", "song"], name="album_song_unique"),
            models.UniqueConstraint(fields=["album", "track_number"], name="album_track_number_unique"),
            models.CheckConstraint(condition=models.Q(track_number__gt=0), name="track_number_positive"),
        ]

