from rest_framework import serializers  # type: ignore
from blogs.models import BlogPost
from comments.models import UserComments
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from likes.models import Like
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class BlogPostWithComments(serializers.ModelSerializer):
    """
    Serializer used for printing comment list
    """

    user_name = serializers.StringRelatedField(
        source="user_id.username", read_only=True
    )

    class Meta:
        model = UserComments
        fields = ["user_name", "content", "date_posted"]
        read_only_fields = ["user_name", "date_posted"]


class BlogPostLikeSerializer(serializers.ModelSerializer):
    """
    Setializer used for printing likes list
    """

    class Meta:
        model = Like
        fields = ["user", "created_at"]
        read_only_fields = ["user", "created_at"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token serializer to include username, id, and email in the token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["firstname"] = user.first_name
        token["lastname"] = user.last_name
        return token


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the details perticular blog.
    """

    comments = BlogPostWithComments(many=True)
    likes = BlogPostLikeSerializer(many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["title", "content", "author", "likes", "comments"]
        read_only_fields = ["comments", "likes"]

    def get_author(self, obj):
        return BlogPost.objects.get(id=obj.id).author.username


class BlogPostListSerializer(serializers.ModelSerializer):
    """
    This serializer is used for listing blog posts
    """

    created_by = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["title", "content", "created_by"]
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)

    def get_created_by(self, obj):
        post = BlogPost.objects.get(id=obj.id)
        return f"{post.author} : {post.author.email} On {post.date_published.strftime('%Y-%m-%d %H:%M:%S')}"
