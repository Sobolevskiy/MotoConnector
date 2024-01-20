from rest_framework_gis import serializers

from motomap.models import Place


class PointSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = ('id', 'name', 'place_type')
        geo_field = 'location'
        model = Place
