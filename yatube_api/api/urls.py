from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

router_v1 = DefaultRouter()
router_v1.register(r'groups', GroupViewSet, basename='group')
router_v1.register(r'posts', PostViewSet, basename='post')
router_v1.register(r'comments', CommentViewSet, basename='comment')
router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/posts/<int:post_id>/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
