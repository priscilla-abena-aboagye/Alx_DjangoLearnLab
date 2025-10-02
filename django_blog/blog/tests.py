from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.other = User.objects.create_user(username="bob", password="pass1234")
        self.post = Post.objects.create(title="Hello", content="Content", author=self.user)

    def test_post_list_view(self):
        resp = self.client.get(reverse("post-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Hello")

    def test_create_requires_login(self):
        resp = self.client.get(reverse("post-create"))
        self.assertNotEqual(resp.status_code, 200) 
        self.client.login(username="alice", password="pass1234")
        resp = self.client.get(reverse("post-create"))
        self.assertEqual(resp.status_code, 200)

    def test_only_author_can_edit(self):
        self.client.login(username="bob", password="pass1234")
        resp = self.client.get(reverse("post-update", kwargs={"pk": self.post.pk}))
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username="alice", password="pass1234")
        resp = self.client.get(reverse("post-update", kwargs={"pk": self.post.pk}))
        self.assertEqual(resp.status_code, 200)
