from rest_framework import serializers
from .models import Author, Book
import datetime

# the book serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

# validates the year. Year can not be in the future
    def validate_publication_year(self, year):
        current_year = datetime.date.today().year
        if year > current_year:
            raise serializers.ValidationError("Year can not be in the future")
        return year

# the serializer for author
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True) # the relationship

    class Meta:
        model = Author
        fields = ["id", "name", "books"] 