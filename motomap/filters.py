import django_filters

from motomap.models import Place


class PlaceTypeFilter(django_filters.FilterSet):
    place_type = django_filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = Place
        fields = ('place_type',)
