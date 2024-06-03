import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestPostListView:
    def test_post_list_view(self, client, published_post, draft_post):
        response = client.get(reverse("blog:post_list"))

        assert response.status_code == 200
        assert published_post.title in response.content.decode()
        assert draft_post.title not in response.content.decode()
        assert "blog/post/list.html" in [t.name for t in response.templates]
        assert "blog/post/pagination.html" in [
            t.name for t in response.templates
        ]
        assert "Page 1 of 1" in response.content.decode()

    def test_post_list_view_pagination(
        self, client, multiple_published_posts_5
    ):
        response = client.get(reverse("blog:post_list"))
        assert response.status_code == 200
        assert len(response.context["posts"]) == 3
        assert "Page 1 of 2" in response.content.decode()

        response = client.get(reverse("blog:post_list"), {"page": 2})
        assert response.status_code == 200
        assert len(response.context["posts"]) == 2
        assert "Page 2 of 2" in response.content.decode()

    def test_post_list_view_pagination_page_not_an_integer(
        self, client, multiple_published_posts_5
    ):
        response = client.get(reverse("blog:post_list"), {"page": "abc"})
        assert response.status_code == 200
        assert len(response.context["posts"]) == 3
        assert "Page 1 of 2" in response.content.decode()

    def test_post_list_pagination_out_of_range(
        self, client, multiple_published_posts_5
    ):
        """
        This test will make sure that when the page is out of range,
        we return the last page.
        """
        response = client.get(reverse("blog:post_list"), {"page": 99})
        assert response.status_code == 200
        assert len(response.context["posts"].object_list) == 2
        assert "Page 2 of 2" in response.content.decode()

    def test_post_detail_view(self, client, published_post):
        response = client.get(
            reverse(
                "blog:post_detail",
                kwargs={
                    "year": published_post.publish.year,
                    "month": published_post.publish.month,
                    "day": published_post.publish.day,
                    "post": published_post.slug,
                },
            )
        )

        assert response.status_code == 200
        assert published_post.title in response.content.decode()
        assert published_post.body in response.content.decode()
        assert "blog/post/detail.html" in [t.name for t in response.templates]

    def test_post_view_not_found(self, client, draft_post):
        response = client.get(
            reverse(
                "blog:post_detail",
                kwargs={
                    "year": draft_post.publish.year,
                    "month": draft_post.publish.month,
                    "day": draft_post.publish.day,
                    "post": draft_post.slug,
                },
            )
        )

        assert response.status_code == 404
