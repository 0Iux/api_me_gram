from rest_framework.serializers import (
    ModelSerializer, CurrentUserDefault,
    SlugRelatedField
)
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['post', 'author']


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault())
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs.get('following')
        if user == following:
            raise ValidationError('Нельзя подписываться на самого себя.')
        return attrs
