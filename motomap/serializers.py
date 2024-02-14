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
    count = serializers.SerializerMethodField(read_only=True)

    def get_count(self, obj):
        return Place.objects.filter(tags=obj).count()

    class Meta:
        model = PlaceTag
        fields = ('id', 'name', 'count')


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


class PlaceImageSerializer(serializers.ModelSerializer):
    height = serializers.SerializerMethodField(read_only=True)
    width = serializers.SerializerMethodField(read_only=True)
    def get_height(self, obj):
        return obj.image.height
    def get_width(self, obj):
        return obj.image.width

    class Meta:
        model = PlaceImage
        fields = ('id', 'image', 'height', 'width')


class FormDataListField(serializers.ListField):
    def _check_if_integer_form_data(self, data):
        if isinstance(self.child, serializers.IntegerField):
            if len(data) >= 1 and isinstance(data[0], str):
                return len(data[0].split(',')) > 1

    def to_internal_value(self, data):
        if self._check_if_integer_form_data(data):
            data = list(map(int, data[0].split(',')))
        return super().to_internal_value(data)


class PlaceSerializer(PointSerializer):
    images = PlaceImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        allow_empty=True,
        required=False,
        write_only=True
    )
    remove_images = FormDataListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        fields = ('id', 'name', 'place_type', 'tags', 'landscapes',
                  'new_tags', 'images', 'upload_images', 'remove_images')
        geo_field = 'location'
        model = Place

    @staticmethod
    def _bulk_image_create(upload_images, instance):
        if upload_images:
            upload_images_list = []
            for image in upload_images:
                new_image = PlaceImage(image=image, place=instance)
                upload_images_list.append(new_image)
            if upload_images_list:
                PlaceImage.objects.bulk_create(upload_images_list)

    def create(self, validated_data):
        upload_images = validated_data.pop('upload_images', None)
        validated_data.pop('remove_images', None)
        instance = super().create(validated_data)
        self._bulk_image_create(upload_images, instance)
        return instance

    def update(self, instance, validated_data):
        upload_images = validated_data.pop('upload_images', None)
        self._bulk_image_create(upload_images, instance)
        remove_images = validated_data.pop('remove_images', None)
        if remove_images:
            PlaceImage.objects.filter(pk__in=remove_images).delete()
        return instance
