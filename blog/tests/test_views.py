import pytest
from django.urls import reverse

from ..models import Post
from .factories import PostFactory


@pytest.mark.django_db
class TestPostListView:
    def test_post_list_view(self, client, published_post, draft_post):
        response = client.get(reverse("blog:post_list"))

        assert response.status_code == 200
        assert published_post.title in response.content.decode()
        assert draft_post.title not in response.content.decode()
        assert "blog/post/list.html" in [t.name for t in response.templates]

    def test_post_detail_view(self, client, published_post):
        response = client.get(
            reverse("blog:post_detail", kwargs={"id": published_post.id})
        )

        assert response.status_code == 200
        assert published_post.title in response.content.decode()
        assert published_post.body in response.content.decode()
        assert "blog/post/detail.html" in [t.name for t in response.templates]

    def test_post_view_not_found(self, client, draft_post):
        response = client.get(
            reverse("blog:post_detail", kwargs={"id": draft_post.id})
        )

        assert response.status_code == 404
