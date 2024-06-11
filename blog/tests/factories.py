import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

from ..models import Comment, Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f"Post {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    author = factory.SubFactory(UserFactory)
    body = "This is the body content of the post."
    publish = factory.LazyAttribute(lambda obj: timezone.now())
    status = Post.Status.DRAFT


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment

    name = factory.Faker("name")
    email = factory.Faker("email")
    body = factory.Faker("text")
    post = factory.SubFactory(PostFactory)
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)
    active = True
