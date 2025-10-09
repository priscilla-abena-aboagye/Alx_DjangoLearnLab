from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowFeedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.alice = User.objects.create_user(username="alice", password="pwd")
        self.bob = User.objects.create_user(username="bob", password="pwd1")
        self.carol = User.objects.create_user(username="carol", password="pwd2")

    def test_follow_unfollow_and_feed(self):
        # login
        self.client.login(username="alice", password="pwd")

        # follow bob
        resp = self.client.post(reverse("follow"), {"user_id": self.bob.id}, format="json")
        assert resp.status_code == 200

        # unfollow carol (not followed yet) -> still OK
        resp = self.client.post(reverse("unfollow"), {"user_id": self.carol.id}, format="json")
        assert resp.status_code == 200

        # check following list
        resp = self.client.get(reverse("following-list"))
        assert resp.status_code == 200
        data = resp.json()
        assert any(u["username"] == "bob" for u in data)

