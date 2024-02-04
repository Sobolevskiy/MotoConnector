import django_filters

from motomap.models import Place


class InListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(**{self.field_name+f'__{self.lookup_expr}': value.split(',')})
        return qs


class PlaceTypeFilter(django_filters.FilterSet):
    place_type = InListFilter(field_name="place_type", lookup_expr="overlap")
    tags = InListFilter(field_name="tags", lookup_expr="in")
    landscapes = InListFilter(field_name="landscapes", lookup_expr="in")

    class Meta:
        model = Place
        fields = ('place_type', 'tags', 'landscapes')
