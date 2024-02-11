from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_gis import filters

from motomap.models import Place, PlaceTag, Landscape
from motomap.serializers import PointSerializer, DictionarySerializer, PlaceTagSerializer, PlaceSerializer
from motomap.filters import PlaceTypeFilter


class MarkersMapView(TemplateView):
    template_name = 'map.html'


class PointsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    bbox_filter_field = 'location'
    filter_backends = (filters.InBBOXFilter, DjangoFilterBackend)
    filterset_class = PlaceTypeFilter
    queryset = Place.objects.filter(Q(tags__isnull=True) | Q(tags__verified=True))
    serializer_class = PointSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceTagsViewSet(generics.ListAPIView):
    serializer_class = PlaceTagSerializer
    queryset = PlaceTag.objects.all()


class DictionariesViewSet(generics.ListAPIView):
    serializer_class = DictionarySerializer
    queryset = Landscape.objects.all()

    def list(self, request, *args, **kwargs):
        landscapes = self.get_queryset()
        landscapes_serializer = self.get_serializer(landscapes, many=True)
        result_data = {Landscape.__name__.lower(): landscapes_serializer.data}
        return Response(result_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_places_types(request):
    resp = {}
    for place_type in Place.PLACE_TYPES_CHOICES:
        resp[place_type[0]] = place_type[1]
    return Response(resp)
