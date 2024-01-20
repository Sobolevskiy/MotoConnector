from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_gis import filters

from motomap.models import Place
from motomap.serializers import PointSerializer
from motomap.filters import PlaceTypeFilter


class MarkersMapView(TemplateView):
    template_name = 'map.html'


class PointsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    bbox_filter_field = 'location'
    filter_backends = (filters.InBBOXFilter,DjangoFilterBackend)
    filterset_class = PlaceTypeFilter
    filter_fields = ('place_type',)
    queryset = Place.objects.all()
    serializer_class = PointSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_places_types(request):
    resp = {}
    for place_type in Place.PLACE_TYPES_CHOICES:
        resp[place_type[0]] = place_type[1]
    return Response(resp)
