from django.urls import path
from rest_framework import routers

from motomap.views import MarkersMapView, PointsViewSet, DictionariesViewSet, get_places_types

router = routers.DefaultRouter()
router.register(r'places', PointsViewSet, basename='places')

urlpatterns = [
    path("map/", MarkersMapView.as_view()),
    path("place_types/", get_places_types),
    path("dictionaries/", DictionariesViewSet.as_view())
]

urlpatterns += router.urls
