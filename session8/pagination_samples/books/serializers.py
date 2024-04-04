import requests
from rest_framework import serializers

from books.models import Book, Comment


def get_data_from_external_service(some_value):
    print('real get data called!')
    # result = requests.get('http://example.com')
    return 'data'


class CommentSerializer(serializers.ModelSerializer):
    external_data = serializers.SerializerMethodField()

    def get_external_data(self, _):
        return get_data_from_external_service('')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'book', 'user', 'external_data']
        depth = 1


class BookSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    external_data = serializers.SerializerMethodField()

    def get_external_data(self, obj):
        return get_data_from_external_service(obj.title)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'published_date', 'comments', 'external_data']
