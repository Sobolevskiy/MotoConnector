from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from socials.models import Comment, Commentable
from socials.serializers import CommentSerializer, RateCommentSerializer


def _commentable_models_mapper():
    return {x.__name__.lower(): x for x in Commentable.__subclasses__()}


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.user.pk == request.user.pk


class ModelCommentsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    @property
    def _model_name(self):
        return self.kwargs['model']

    @property
    def _get_pk(self):
        return self.kwargs['id']

    def get_queryset(self):
        _model = _commentable_models_mapper().get(self._model_name)
        return self.queryset.filter(content_type=ContentType.objects.get_for_model(_model),
                                    object_id=self._get_pk)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @property
    def _model_name(self):
        return self.kwargs['model']

    def get_queryset(self):
        if self.action == self.list.__name__:
            _model = _commentable_models_mapper().get(self._model_name)
            return self.queryset.filter(content_type=ContentType.objects.get_for_model(_model))
        else:
            return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['model'] = _commentable_models_mapper().get(self._model_name)
        return context

    def create(self, request, *args, **kwargs):
        _models_mapper = _commentable_models_mapper()
        if not _models_mapper.get(self._model_name.lower()):
            return Response(_models_mapper.keys(), status=404)
        else:
            return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post', 'delete'], permission_classes=(IsAuthenticated,))
    def rate(self, request, model=None, pk=None):
        comment = self.get_object()
        user = request.user
        status = 201
        if request.method.lower() == 'post':
            serializer = RateCommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                comment, created = comment.grades.get_or_create(user=user, defaults=serializer.data)
                if not created:
                    comment.grade = serializer.data['grade']
                    comment.save()
            except IntegrityError:
                status = 400
        elif request.method.lower() == 'delete':
            comment = comment.grades.filter(user=user)
            if comment.exists():
                comment.delete()
            status = 204
        else:
            status = 404
        return Response(status=status)


@action(methods=['get'], detail=False)
def get_commentable_models(request):
    return JsonResponse({"models": list(_commentable_models_mapper().keys())}, status=200)
