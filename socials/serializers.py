from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from socials.models import Comment, CommentBinaryGrade


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.pk', read_only=True)
    content_type = serializers.CharField(source='content_type.model', read_only=True)
    grades = serializers.SerializerMethodField(read_only=True)

    def get_grades(self, obj):
        likes = 0
        dislikes = 0
        qs = (obj
              .grades.values("grade")
              .annotate(likes_count=Count('grade', filter=Q(grade=CommentBinaryGrade.LIKE)))
              .annotate(dislikes_count=Count('grade', filter=Q(grade=CommentBinaryGrade.DISLIKE)))
              )
        if qs.exists():
            likes = qs[0]['likes_count']
            dislikes = qs[0]['dislikes_count']
        return {'likes': likes, 'dislikes': dislikes}

    class Meta:
        model = Comment
        fields = ('id', 'object_id', 'content_type', 'comment', 'user', 'grade', 'grades')

    def validate(self, attrs):
        # Проверка, что object_id, на который ссылается действительно существует
        if attrs.get('object_id'):
            try:
                attrs['content_object'] = self.context['model'].objects.get(pk=attrs['object_id'])
            except self.context['model'].DoesNotExist:
                raise serializers.ValidationError(
                    {'object_id': ['Invalid pk [' + str(attrs['object_id']) + '] - object does not exist.']})
        return attrs

    def create(self, validated_data):
        validated_data['content_type'] = ContentType.objects.get_for_model(self.context['model'])
        if self.context.get('request'):
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class RateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentBinaryGrade
        fields = ('grade',)
