from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers

from motomap.models import Place, PlaceTag, PlaceImage


class ImageUrlField(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class DictionarySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)


class PlaceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceTag
        fields = ('id', 'name')


class PointSerializer(gis_serializers.GeoFeatureModelSerializer):
    new_tags = serializers.ListField(
        child=serializers.CharField(required=False),
        allow_empty=True,
        required=False,
        write_only=True
    )

    def create(self, validated_data):
        new_tags = validated_data.pop('new_tags', None)
        if new_tags:
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


class PlaceSerializer(PointSerializer):
    images = ImageUrlField(
        many=True,
        read_only=True
    )
    upload_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        allow_empty=True,
        required=False,
        write_only=True
    )

    class Meta:
        fields = ('id', 'name', 'place_type', 'tags', 'landscapes', 'new_tags', 'images', 'upload_images')
        geo_field = 'location'
        model = Place

    def create(self, validated_data):
        upload_images = validated_data.pop('upload_images', None)
        instance = super().create(validated_data)
        if upload_images:
            upload_images_list = []
            for image in upload_images:
                new_image = PlaceImage(image=image, place=instance)
                upload_images_list.append(new_image)
            if upload_images_list:
                PlaceImage.objects.bulk_create(upload_images_list)

        return instance
