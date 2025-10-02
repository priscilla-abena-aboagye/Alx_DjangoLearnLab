from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

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

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.other = User.objects.create_user(username="bob", password="pass1234")
        self.post = Post.objects.create(title="T", content="C", author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse("comment-create", kwargs={"post_pk": self.post.pk})
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username="bob", password="pass1234")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url, {"content": "Nice post"})
        self.assertRedirects(resp, reverse("post-detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(self.post.comments.count(), 1)
        comment = self.post.comments.first()
        self.assertEqual(comment.author, self.other)

    def test_only_author_can_edit_or_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.other, content="hey")
        update_url = reverse("comment-update", kwargs={"pk": comment.pk})
        delete_url = reverse("comment-delete", kwargs={"pk": comment.pk})

        self.client.login(username="alice", password="pass1234")
        resp = self.client.get(update_url)
        self.assertNotEqual(resp.status_code, 200)
        resp = self.client.get(delete_url)
        self.assertNotEqual(resp.status_code, 200)

        self.client.login(username="bob", password="pass1234")
        resp = self.client.get(update_url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(update_url, {"content": "updated"})
        self.assertRedirects(resp, reverse("post-detail", kwargs={"pk": self.post.pk}))
        comment.refresh_from_db()
        self.assertEqual(comment.content, "updated")
