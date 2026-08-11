from django.db.models import Prefetch, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Album, AlbumTrack, Artist, Song
from .serializers import AddTrackSerializer, AlbumSerializer, ArtistSerializer, SongSerializer, TrackSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        qs = Album.objects.select_related("artist").prefetch_related(
            Prefetch("tracks", AlbumTrack.objects.select_related("song").order_by("track_number"))
        )
        search = self.request.query_params.get("search", "").strip()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(artist__name__icontains=search) | Q(tracks__song__title__icontains=search)).distinct()
        return qs

    @action(detail=True, methods=["post"], url_path="tracks")
    def add_track(self, request, pk=None):
        serializer = AddTrackSerializer(data=request.data, context={"album": self.get_object()})
        serializer.is_valid(raise_exception=True)
        track = serializer.save()
        return Response(TrackSerializer(track).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path=r"tracks/(?P<track_id>[^/.]+)")
    def remove_track(self, request, pk=None, track_id=None):
        track = self.get_object().tracks.filter(pk=track_id).first()
        if not track:
            return Response(status=status.HTTP_404_NOT_FOUND)
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

