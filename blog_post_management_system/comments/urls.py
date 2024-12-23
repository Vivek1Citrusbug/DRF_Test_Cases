from django.urls import path, include
from .views import CommentListView,CommentCreateView,CommentDeleteView

urlpatterns = [
    path("<int:pk>/", CommentListView.as_view(), name="list_comment"),
    path('<int:pk>/new/',CommentCreateView.as_view(), name='create_comment'),
    path('<int:pk>/delete/',CommentDeleteView.as_view(), name='delete_comment'),
]
