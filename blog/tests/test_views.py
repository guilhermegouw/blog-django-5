import pytest
from blog.models import Comment
from django.core import mail
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


@pytest.mark.django_db
class TestPostDetailView:

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


@pytest.mark.django_db
class TestPostShareView:

    def test_post_share_view_get(self, client, published_post):
        response = client.get(
            reverse("blog:post_share", kwargs={"post_id": published_post.id})
        )

        assert response.status_code == 200
        assert "form" in response.context
        assert not response.context["sent"]
        assert "blog/post/share.html" in [t.name for t in response.templates]

    def test_post_share_post_valid(self, client, published_post):
        response = client.post(
            reverse("blog:post_share", kwargs={"post_id": published_post.id}),
            {
                "name": "Jane Doe",
                "email": "test@example.com",
                "to": "receiver@example.com",
                "comments": "Check out this post!",
            },
        )

        assert response.status_code == 200
        assert response.context["sent"]
        assert len(mail.outbox) == 1
        assert (
            mail.outbox[0].subject
            == f"Jane Doe recommends you read {published_post.title}"
        )

    def test_post_share_post_invalid(self, client, published_post):
        response = client.post(
            reverse("blog:post_share", kwargs={"post_id": published_post.id}),
            {
                "name": "",
                "email": "invalid-email",
                "to": "friend@email.com",
                "comments": "This isn't a good post...",
            },
        )
        assert response.status_code == 200
        assert not response.context["sent"]
        assert len(mail.outbox) == 0
        assert response.context["form"].errors


@pytest.mark.django_db
class TestCommentView:

    def test_comment_valid(self, client, published_post):
        response = client.post(
            reverse(
                "blog:post_comment", kwargs={"post_id": published_post.id}
            ),
            {
                "name": "Jane Doe",
                "email": "test@example.com",
                "body": "Great post!",
            },
        )

        assert response.status_code == 200
        assert Comment.objects.filter(post=published_post).exists()
        assert "comment" in response.context
        assert response.context["comment"].body == "Great post!"
