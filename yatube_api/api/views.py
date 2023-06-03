from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, pagination, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.author:
            raise PermissionDenied("You are not the author of this post.")
        super().perform_update(serializer)

    def perform_destroy(self, obj):
        if self.request.user != obj.author:
            raise PermissionDenied("You are not the author of this post.")
        super().perform_destroy(obj)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.author:
            raise PermissionDenied("You are not the author of this post.")
        super().perform_update(serializer)

    def perform_destroy(self, obj):
        if self.request.user != obj.author:
            raise PermissionDenied("You are not the author of this post.")
        super().perform_destroy(obj)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)


class FollowViewSet(viewsets.ModelViewSet):
    pass
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#     permission_classes = (permissions.IsAuthenticated,)
