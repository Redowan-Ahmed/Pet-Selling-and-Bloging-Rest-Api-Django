from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name','slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_title']


class PostCommentReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentReplay
        fields = ['reply', 'user', 'created_at']


class PostCommentSerializer(serializers.ModelSerializer):
    post_comment_reply = PostCommentReplaySerializer(many=True)

    class Meta:
        model = PostComment
        fields = ['title', 'comment', 'user','post_comment_reply', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    post_comments = PostCommentSerializer(many=True)
    tag = TagSerializer(many=True)
    author = UserSerializer()
    class Meta:
        model = Post
        fields = '__all__'
