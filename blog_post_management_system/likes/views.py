from django.shortcuts import render
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from blogs.models import BlogPost
from django.views.generic import DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BlogPost, Like

# Create your views here.


@method_decorator(login_required, name="dispatch")
class LikeView(View):
    """This view is used to like user blogs"""

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, pk=self.kwargs["pk"])
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()

        return redirect("blog_detail", pk=post.pk)
