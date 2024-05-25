import pytest
from django.utils.text import slugify

from ..models import Post
from .factories import PostFactory


@pytest.mark.django_db
class TestPostModel:
    def test_post_model_creation(self):
        post = PostFactory()
        assert isinstance(post, Post)
        assert post.title.startswith("Post")
        assert post.body == "This is the body content of the post."
        assert post.slug == slugify(post.title)

    def test_post_model_str(self):
        post = PostFactory(title="Test Post")
        assert str(post) == "Test Post"


@pytest.mark.django_db
class TestPostManager:
    def test_published_manager(self):
        published_post = PostFactory(status=Post.Status.PUBLISHED)
        draft_post = PostFactory(status=Post.Status.DRAFT)

        published_posts = Post.published.all()
        assert published_post in published_posts
        assert draft_post not in published_posts
