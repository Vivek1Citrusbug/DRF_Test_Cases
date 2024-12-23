from django.test import TestCase
from django.contrib.auth.models import User
from blogs.models import BlogPost
from django.utils import timezone
from django.core.exceptions import ValidationError


class UserProfileModelTestCases(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "test title",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "date_published": timezone.now(),
        }
        self.user = User.objects.create_user(username="username", password="password")
        self.blog_post = BlogPost.objects.create(**self.valid_data, author=self.user)

    def test_blog_post_creation(self):
        """Test that the BlogPost model creates a blog post correctly"""

        self.assertEqual(self.blog_post.title, self.valid_data["title"])
        self.assertEqual(self.blog_post.content, self.valid_data["content"])
        self.assertEqual(self.blog_post.author, self.user)

    def test_blog_post_str_method(self):
        """Test that the __str__ method returns the correct title"""

        self.assertEqual(str(self.blog_post), self.valid_data["title"])

    def test_likes_count_field(self):
        """Test the likes_count Many-to-Many field"""

        another_user = User.objects.create_user(
            username="anotheruser", password="testpassword2"
        )
        self.blog_post.likes_count.add(another_user)
        self.assertIn(another_user, self.blog_post.likes_count.all())
        self.assertEqual(self.blog_post.likes_count.count(), 1)

    def test_blog_post_without_required_fields(self):
        """Test the blog post creation without title and content fields"""

        blog_without_required = BlogPost(title="", content="", author=self.user)

        with self.assertRaises(ValidationError):
            blog_without_required.full_clean()

    def test_blog_post_date_published_default(self):
        """Test that the date_published field uses the current time if not provided"""

        blog_post_without_date = BlogPost.objects.create(
            title="Blog Post without date",
            content="This post has no specific date.",
            author=self.user,
        )
        self.assertIsNotNone(blog_post_without_date.date_published)
        self.assertEqual(
            blog_post_without_date.date_published.date(), timezone.now().date()
        )

    def test_blog_post_likes_count_is_blank_by_default(self):
        """Test that the likes_count field is blank by default"""

        self.assertEqual(self.blog_post.likes_count.count(), 0)