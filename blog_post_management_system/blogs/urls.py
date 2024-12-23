from .views import BlogCreateView,BlogDetailView,BlogPostDeleteView,BlogPostListingView,BlogUpdateView
from django.urls import path,include
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'Blogs',BlogPostListingAPIView,basename='blogpost')

urlpatterns = [
    # path("",include(router.urls))
    path('', BlogPostListingView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),
    path('new/', BlogCreateView.as_view(), name='blog_create'),
]