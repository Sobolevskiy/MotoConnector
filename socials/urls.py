from django.urls import path
from rest_framework import routers

from socials.views import CommentViewSet, ModelCommentsViewSet, get_commentable_models

router = routers.DefaultRouter()
router.register(r'(?P<model>[\w-]+)/comment', CommentViewSet, basename='comment')
router.register(r'(?P<model>[\w-]+)/(?P<id>[\w-]+)/comments', ModelCommentsViewSet, basename='model_comments')

urlpatterns = [
    path("commentable_models/", get_commentable_models),
]

urlpatterns += router.urls
