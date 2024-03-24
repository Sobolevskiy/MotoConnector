from django.contrib import admin

from .models import Comment, CommentBinaryGrade


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_type', 'object_id', 'grade')
    list_filter = ('content_type', 'grade')


@admin.register(CommentBinaryGrade)
class CommentBinaryGradeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'comment', 'grade')
