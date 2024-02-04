from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers

from motomap.models import Place, PlaceTag


class DictionarySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    model = serializers.SerializerMethodField()

    @staticmethod
    def get_model(obj):
        return obj.__class__.__name__.lower()


class PointSerializer(gis_serializers.GeoFeatureModelSerializer):
    new_tags = serializers.ListField(
        child=serializers.CharField(required=False),
        allow_empty=True,
        required=False,
        write_only=True
    )

    def create(self, validated_data):
        new_tags = validated_data.pop('new_tags')
        new_tags_list = []
        for tag in new_tags:
            found_tag, _ = PlaceTag.objects.get_or_create(name=tag)
            new_tags_list.append(found_tag)
        validated_data['tags'] += new_tags_list
        return super().create(validated_data)

    class Meta:
        fields = ('id', 'name', 'place_type', 'tags', 'landscapes', 'new_tags')
        geo_field = 'location'
        model = Place
