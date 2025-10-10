from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class FollowFeedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.alice = User.objects.create_user(username="alice", password="pwd")
        self.bob = User.objects.create_user(username="bob", password="pwd")
        self.carol = User.objects.create_user(username="carol", password="pwd2")

    def test_follow_unfollow_and_feed(self):
        # login
        self.client.force_authenticate(user=self.alice)

        # follow bob
        resp = self.client.post(reverse("follow", args=[self.bob.id]), format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK) 

        # self.alice.refresh_from_db()

        # check following list
        resp = self.client.get(reverse("following-list"))
        assert resp.status_code == 200
        data = resp.json()
        print("FOLLOWING LIST DATA:", data)
        self.assertTrue(any(u["username"] == "bob" for u in data))

