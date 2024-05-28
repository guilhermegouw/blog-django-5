import pytest

from ..models import Post
from .factories import PostFactory


@pytest.fixture
def published_post():
    return PostFactory(status=Post.Status.PUBLISHED)


@pytest.fixture
def draft_post():
    return PostFactory(status=Post.Status.DRAFT)
