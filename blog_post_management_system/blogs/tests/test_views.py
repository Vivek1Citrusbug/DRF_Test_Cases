from rest_framework.test import APITestCase
from blogs.tests.test_setup import TestSetUp, CommentSetup
from rest_framework import status
from blogs.models import BlogPost
from django.urls import reverse


class TestBlogAPI(TestSetUp):

    def test_list_blog_posts_authenticated(self):
        """
        Test listing blog posts with an authenticated user.
        """

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_list_blog_posts_unauthenticated(self):
        """
        Test listing blog posts without authentication.
        """

        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_blog_post_authenticated(self):
        """
        Test retrieving a single blog post with an authenticated user.
        """

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.blog1.title)

    def test_retrieve_blog_post_unauthenticated(self):
        """
        Test retrieving a single blog post without authentication.
        """

        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_blog_post_authenticated(self):
        """
        Test creating a blog post with an authenticated user.
        """

        data = {
            "title": "New Blog Post",
            "content": "New Content",
            "likes_count": 0,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 3)

    def test_create_blog_post_unauthenticated(self):
        """
        Test creating a blog post without authentication.
        """

        self.client.logout()
        data = {
            "title": "New Blog Post",
            "content": "New Content",
            "likes_count": 0,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_blog_post_authenticated(self):
        """
        Test updating a blog post with an authenticated user.
        """

        data = {"title": "Updated Title"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.title, "Updated Title")

    def test_update_blog_post_unauthenticated(self):
        """
        Test updating a blog post without authentication.
        """

        self.client.logout()
        data = {"title": "Updated Title"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_blog_post_authenticated(self):
        """
        Test deleting a blog post with an authenticated user.
        """

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogPost.objects.filter(id=self.blog1.id).exists())

    def test_delete_blog_post_unauthenticated(self):
        """
        Test deleting a blog post without authentication.
        """

        self.client.logout()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ordering_blog_posts(self):
        """
        Test ordering blog posts by a specified field.
        """

        response = self.client.get(self.list_url, {"ordering": "-date_published"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertIn(str(self.blog2.date_published), results[0]["created_by"])
        self.assertIn(str(self.blog1.date_published), results[1]["created_by"])


class TestCommentAPI(CommentSetup):

    def test_get_comments_success(self):
        """
        Test comments listing
        """

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.context)
        comments = response.context["comments"]
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].content, self.comment1.content)
        self.assertEqual(comments[1].content, self.comment2.content)

    def test_get_comments_invalid_blog_post_id(self):
        url = reverse("blog_detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

