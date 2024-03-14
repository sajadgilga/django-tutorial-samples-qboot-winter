from rest_framework import serializers

from books.models import Book, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'book', 'user']
        depth = 1


class BookSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'published_date', 'comments']
