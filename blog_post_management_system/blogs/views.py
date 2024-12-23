from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import BlogPost
from comments.models import UserComments
from .forms import BlogPostForm
from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from blogs.serializers import (
    BlogPostLikeSerializer,
    BlogPostWithComments,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, BaseFilterBackend
from blogs.general import MyPaginator, MyOrderingFilter
from blogs.serializers import (
    CustomTokenObtainPairSerializer,
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    BlogPostWithComments,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from blogs.general import api_exception_handler
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class BlogPostListingAPIView(ModelViewSet):
    """Blog post list view to fetch list of blogs of users.
    Used JWT authentication for authorizing user."""

    permission_classes = [IsAuthenticated]
    pagination_class = MyPaginator
    filter_backends = [MyOrderingFilter]
    ordering_fields = ["date_published", "total_likes"]

    def get_serializer_class(self):
        if self.action in ["list", "update", "create", "partial_update"]:
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def get_queryset(self):
        return BlogPost.objects.all()

    @extend_schema(
        tags=["Blog API"],
        summary="List all blog posts",
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Specify the field to order by. Prefix with '-' for descending order. Available fields: 'date_published', 'total_likes'.",
                required=False,
                type=OpenApiTypes.STR,
                enum=[
                    "date_published",
                    "-date_published",
                    "total_likes",
                    "-total_likes",
                ],
            ),
        ],
        description="Fetch a list of all blog posts with optional filtering and pagination.",
        responses={200: BlogPostListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """Default list method with extended schema."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=["Blog API"],
        summary="Retrieve a single blog post",
        description="Fetch detailed information about a specific blog post.",
        responses={200: BlogPostDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        """Default retrieve method with extended schema."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Blog API"],
        summary="Create a new blog post",
        description="Create a new blog post. Requires authentication.",
        request=BlogPostListSerializer,
        responses={201: BlogPostDetailSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Default create method with extended schema."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=["Blog API"],
        summary="Update an existing blog post",
        description="Partially update an existing blog post. Requires authentication.",
        request=BlogPostListSerializer,
        responses={200: BlogPostDetailSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        """Default partial_update method with extended schema."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["Blog API"],
        summary="Update an existing blog post",
        description="Update an existing blog post. Requires authentication.",
        request=BlogPostListSerializer,
        responses={200: BlogPostDetailSerializer},
    )
    def update(self, request, *args, **kwargs):
        """Default update method with extended schema."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=["Blog API"],
        summary="Delete a blog post",
        description="Delete a blog post by its ID. Requires authentication.",
        responses={204: "Blog successfully deleted"},
    )
    def destroy(self, request, *args, **kwargs):
        """Default destroy method with extended schema."""
        return super().destroy(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    """Comment list view for listing out comments"""

    serializer_class = BlogPostWithComments

    def get_queryset(self):
        blog_post_id = self.kwargs["blog_post_id"]
        return UserComments.objects.filter(post_id=blog_post_id)

    @extend_schema(
        tags=["Blog API"],
        summary="List comments",
        description="List comments of given blog",
        responses={200: "Listed all the comments"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    tags=["Authentication"],
    summary="Refresh JWT Token",
    description="Refresh an expired access token using a valid refresh token.",
    request=TokenRefreshSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {
                    "type": "string",
                    "description": "Newly generated access token.",
                },
                "refresh": {
                    "type": "string",
                    "description": "Optional. New refresh token if issued.",
                },
            },
        },
        400: {
            "type": "object",
            "properties": {
                "detail": {
                    "type": "string",
                    "description": "Error message for invalid token or other issues.",
                },
            },
        },
    },
)
class CustomTokenRefreshView(TokenRefreshView):
    """
    A custom view for refreshing JWT tokens.
    """

    pass


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining a pair of JWT tokens (access and refresh).
    This view uses the custom serializer to include additional data in the token.
    """

    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        tags=["Authentication"],
        description="Obtain a new JWT token.",
        request=TokenObtainPairSerializer,
        responses={200: TokenObtainPairSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BlogPostListingView(LoginRequiredMixin, ListView):
    """This view is used to list all the blogs"""

    model = BlogPost
    template_name = "blogs/blog_list.html"
    context_object_name = "posts"
    ordering = ["-date_published"]


class BlogDetailView(LoginRequiredMixin, DetailView):
    """This view is used to give detail of selected blog"""

    model = BlogPost
    template_name = "blogs/blog_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["likes_count"] = post.likes.count()
        context["user_liked"] = post.likes.filter(user=self.request.user).exists()
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    """This view is used to create new blog"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogs/blog_form.html"
    success_url = reverse_lazy("blog_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """This view is used to update existing blog"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogs/blog_form.html"
    success_url = reverse_lazy("blog_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """This view is used to delete existing blog"""

    model = BlogPost
    template_name = "blogs/blog_confirm_delete.html"
    success_url = reverse_lazy("blog_list")
    context_object_name = "post"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff
