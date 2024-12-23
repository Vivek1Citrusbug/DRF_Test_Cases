from django.urls import path,include
from .views import LikeView

urlpatterns = [
    path('like/<int:pk>/', LikeView.as_view(), name='like_post'),
]