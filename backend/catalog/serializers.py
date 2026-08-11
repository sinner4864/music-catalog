from django.db import IntegrityError, transaction
from rest_framework import serializers
from .models import Album, AlbumTrack, Artist, Song


class SafeCreateModelSerializer(serializers.ModelSerializer):
    conflict_message = "Объект с такими данными уже существует."

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError as exc:
            raise serializers.ValidationError({"detail": self.conflict_message}) from exc


class ArtistSerializer(SafeCreateModelSerializer):
    conflict_message = "Такой исполнитель уже существует."

    class Meta:
        model = Artist
        fields = ["id", "name"]

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Введите имя исполнителя.")
        if Artist.objects.filter(name__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Такой исполнитель уже существует.")
        return value


class SongSerializer(SafeCreateModelSerializer):
    conflict_message = "Такая песня уже существует."

    class Meta:
        model = Song
        fields = ["id", "title"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Введите название песни.")
        if Song.objects.filter(title__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Такая песня уже существует.")
        return value


class TrackSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)

    class Meta:
        model = AlbumTrack
        fields = ["id", "track_number", "song"]


class AlbumSerializer(SafeCreateModelSerializer):
    conflict_message = "У исполнителя уже есть такой альбом."

    artist_name = serializers.CharField(source="artist.name", read_only=True)
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "artist_name", "release_year", "tracks"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Введите название альбома.")
        return value

    def validate(self, attrs):
        artist = attrs.get("artist", getattr(self.instance, "artist", None))
        title = attrs.get("title", getattr(self.instance, "title", ""))
        qs = Album.objects.filter(artist=artist, title__iexact=title)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"title": "У исполнителя уже есть такой альбом."})
        return attrs


class AddTrackSerializer(serializers.Serializer):
    song_id = serializers.PrimaryKeyRelatedField(source="song", queryset=Song.objects.all(), required=False)
    song_title = serializers.CharField(max_length=250, required=False)
    track_number = serializers.IntegerField(min_value=1, max_value=32767)

    def validate(self, attrs):
        if bool(attrs.get("song")) == bool(attrs.get("song_title")):
            raise serializers.ValidationError("Укажите song_id или song_title.")
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                album = self.context["album"]
                song = validated_data.get("song")
                if song is None:
                    title = validated_data.pop("song_title").strip()
                    if not title:
                        raise serializers.ValidationError({"song_title": "Введите название песни."})
                    song = Song.objects.filter(title__iexact=title).first() or Song.objects.create(title=title)
                if album.tracks.filter(song=song).exists():
                    raise serializers.ValidationError({"song": "Песня уже есть в этом альбоме."})
                if album.tracks.filter(track_number=validated_data["track_number"]).exists():
                    raise serializers.ValidationError({"track_number": "Этот номер уже занят."})
                return AlbumTrack.objects.create(
                    album=album,
                    song=song,
                    track_number=validated_data["track_number"],
                )
        except IntegrityError as exc:
            raise serializers.ValidationError(
                {"detail": "Песня или номер трека уже используются в этом альбоме."}
            ) from exc
