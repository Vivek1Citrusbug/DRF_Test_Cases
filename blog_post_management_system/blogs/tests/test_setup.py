from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from blogs.models import BlogPost
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework.test import APIClient
from comments.models import UserComments


class TestSetUp(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.blog1 = BlogPost.objects.create(
            title="Blog Post 1",
            content="Content 1",
            author=self.user,
            date_published=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        self.blog2 = BlogPost.objects.create(
            title="Blog Post 2",
            content="Content 2",
            author=self.user,
            date_published=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.list_url = "/api/blogs/"
        self.detail_url = f"/api/blogs/{self.blog1.pk}/"
        self.client.login(username="testuser", password="testpassword")
        super().setUp()

    def tearDown(self):
        return super().tearDown()

class CommentSetup(APITestCase):
   
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.blog_post = BlogPost.objects.create(title="Test Blog", content="Test Content", author=self.user)
        self.comment1 = UserComments.objects.create(post_id=self.blog_post, user_id=self.user, content="First Comment")
        self.comment2 = UserComments.objects.create(post_id=self.blog_post, user_id=self.user, content="Second Comment")      
        
        self.client = APIClient()
        self.client.login(username="testuser", password="password")
        self.list_url = reverse("list_comment", kwargs={"pk": self.blog_post.pk})

