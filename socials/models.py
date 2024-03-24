from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class BinaryGrade(models.Model):
    """ Оценка, которая может быть Лайк/Дизлайк """
    LIKE = 20
    DISLIKE = 0
    GRADE_CHOICES = (
        (LIKE, 'Лайк'),
        (DISLIKE, 'Дизлайк'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Comment(models.Model):
    LIKE = 20
    NEUTRAL = 10
    DISLIKE = 0
    GRADE_CHOICES = (
        (LIKE, 'Лайк'),
        (NEUTRAL, 'Нейтрально'),
        (DISLIKE, 'Дизлайк'),
    )

    # GenericRelation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    grade = models.IntegerField(choices=GRADE_CHOICES)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Commentable(models.Model):
    comments = GenericRelation(Comment)

    class Meta:
        abstract = True


class CommentBinaryGrade(BinaryGrade):
    comment = models.ForeignKey(Comment, related_name="grades", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name='unique_user_comment_grade')
        ]
