from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class FeedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.alice = User.objects.create_user(username="alice", password="pwd")
        self.bob = User.objects.create_user(username="bob", password="pwd1")
        # bob posts
        Post.objects.create(author=self.bob, title="Hello", content="From Bob")
        Post.objects.create(author=self.bob, title="Another", content="From Bob")

    def test_feed_shows_followed_posts(self):
        self.client.login(username="alice", password="pwd")
        # Alice follows Bob
        self.alice.follow(self.bob)
        resp = self.client.get(reverse("feed"))
        assert resp.status_code == 200
        body = resp.json()
        assert body["results"]  # pagination
        assert any(p["title"] == "Hello" for p in body["results"])

