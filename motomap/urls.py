from django.urls import path
from rest_framework import routers

from motomap.views import MarkersMapView, PointsViewSet, DictionariesViewSet, PlaceTagsViewSet

router = routers.DefaultRouter()
router.register(r'places', PointsViewSet, basename='places')

urlpatterns = [
    path("map/", MarkersMapView.as_view()),
    path("dictionaries/", DictionariesViewSet.as_view()),
    path("place_tags/", PlaceTagsViewSet.as_view()),
]

urlpatterns += router.urls
