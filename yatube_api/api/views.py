from django.shortcuts import get_object_or_404
from rest_framework import (
    status, viewsets, pagination,
    permissions, filters
)
from rest_framework.exceptions import (
    PermissionDenied, ValidationError
)
from rest_framework.response import Response


from .permissions import AuthorOrReadOnly, ReadOnly
from posts.models import Comment, Group, Post, Follow
from .serializers import (
    CommentSerializer, GroupSerializer,
    PostSerializer, FollowSerializer
)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
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
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username', '=following__username')

    def perform_create(self, serializer):
        user = self.request.user
        following = serializer.validated_data.get('following')
        if user == following:
            raise ValidationError("You cannot follow yourself.")
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError("You are already following this user.")
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
