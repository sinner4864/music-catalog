from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, ArtistViewSet, SongViewSet

router = DefaultRouter()
router.register("artists", ArtistViewSet)
router.register("songs", SongViewSet)
router.register("albums", AlbumViewSet, basename="album")
urlpatterns = router.urls

