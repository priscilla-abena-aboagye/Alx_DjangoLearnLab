from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="Kitty", password="Kitty1234")
        self.client.login(username="Kitty", password="Kitty1234")

        # Creting a user
        self.author = Author.objects.create(name="J.K. Rowling")

        # Creating a book
        self.book = Book.objects.create(
            title="Love and Hate",
            publication_year=1997,
            author=self.author
        )
        # should match the urls
        self.list_url = reverse("book-list-api")
        self.detail_url = reverse("book-detail-api", kwargs={"pk": self.book.id})


    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        self.client.logout()
        data = {"title": "Unauthorized Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        data = {"title": "Updated Title", "publication_year": 1997, "author": self.author.id}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {"author": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["author"], self.author.id)

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {"search": "Love"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Love and Hate", response.data[0]["title"])

    def test_order_books_by_year(self):
        Book.objects.create(title="Another love", publication_year=2005, author=self.author)
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))