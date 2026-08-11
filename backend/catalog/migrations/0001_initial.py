import catalog.models
import django.db.models.deletion
from django.db import migrations, models
from django.db.models.functions import Lower


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Artist", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200))], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Song", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=250))], options={"ordering": ["title"]}),
        migrations.CreateModel(name="Album", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=250)), ("release_year", models.PositiveSmallIntegerField(validators=[catalog.models.validate_release_year])), ("artist", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="albums", to="catalog.artist"))], options={"ordering": ["-release_year", "title"]}),
        migrations.CreateModel(name="AlbumTrack", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("track_number", models.PositiveSmallIntegerField()), ("album", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tracks", to="catalog.album")), ("song", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="track_entries", to="catalog.song"))], options={"ordering": ["track_number"]}),
        migrations.AddField(model_name="album", name="songs", field=models.ManyToManyField(related_name="albums", through="catalog.AlbumTrack", to="catalog.song")),
        migrations.AddConstraint(model_name="artist", constraint=models.UniqueConstraint(Lower("name"), name="artist_name_ci_unique")),
        migrations.AddConstraint(model_name="song", constraint=models.UniqueConstraint(Lower("title"), name="song_title_ci_unique")),
        migrations.AddConstraint(model_name="album", constraint=models.UniqueConstraint(Lower("title"), "artist", name="album_artist_title_ci_unique")),
        migrations.AddConstraint(model_name="albumtrack", constraint=models.UniqueConstraint(fields=("album", "song"), name="album_song_unique")),
        migrations.AddConstraint(model_name="albumtrack", constraint=models.UniqueConstraint(fields=("album", "track_number"), name="album_track_number_unique")),
        migrations.AddConstraint(model_name="albumtrack", constraint=models.CheckConstraint(condition=models.Q(("track_number__gt", 0)), name="track_number_positive")),
    ]

