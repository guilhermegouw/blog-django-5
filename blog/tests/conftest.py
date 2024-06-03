import pytest

from ..models import Post
from .factories import PostFactory


@pytest.fixture
def published_post():
    return PostFactory(status=Post.Status.PUBLISHED)


@pytest.fixture
def multiple_published_posts_5():
    return PostFactory.create_batch(5, status=Post.Status.PUBLISHED)


@pytest.fixture
def draft_post():
    return PostFactory(status=Post.Status.DRAFT)
