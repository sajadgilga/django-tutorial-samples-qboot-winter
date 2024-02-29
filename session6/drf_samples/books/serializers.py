from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from books.models import Book, Comment


def check_unique_title(value):
    print(f'value is: {value}')
    if Book.objects.filter(title=value).exists():
        raise ValidationError('title must be unique')


def check_min_length(value):
    if len(value) < 3:
        raise ValidationError('title length must be more than 3')


def validate_book():
    def validate(attrs, serializer=None):
        print(attrs)
        print(serializer)

    return validate


class CommentLeanSerializer(serializers.Serializer):
    text = serializers.CharField()
    user_id = serializers.IntegerField(write_only=True)


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=True, validators=[check_unique_title, check_min_length])
    description = serializers.CharField()
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    info = serializers.CharField(read_only=True)
    published_date = serializers.DateField(allow_null=True, required=False, initial='2022-10-10')
    comments = CommentLeanSerializer(many=True)

    # def get_comments(self, obj):
    #     # any desired logic
    #     return CommentLeanSerializer(obj.comments, many=True).data

    def validate_title(self, value):
        check_unique_title(value)
        if len(value) > 10:
            raise ValidationError("title must be less than 10 chars")
        # value = value.lower()
        return value

    def validate_published_date(self, value):
        if value > datetime.now().date():
            raise ValidationError("published date must be less than current time")
        return value

    def validate(self, data):
        if data['title'] == data['description']:
            raise ValidationError("title & description must not match")
        return data

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Book.objects.all(), fields=('title', 'description')),
                      validate_book()]

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.author_id = validated_data['author_id']
        instance.published_date = validated_data['published_date']
        instance.description = validated_data['description']
        instance.save()
        return instance

    def create(self, validated_data):
        some_condition = validated_data.pop('something')
        comments = validated_data.pop('comments')
        if some_condition:
            book = Book.objects.create(**validated_data)
        else:
            validated_data['author_id'] = 1
            book = Book.objects.create(**validated_data)
        for comment in comments:
            Comment.objects.create(**comment, book=book)
        return book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user_name = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['book', 'text', 'id', 'user', 'user_name']
        depth = 1

    def get_user_name(self, obj: Comment):
        return obj.user.first_name + ' ' + obj.user.last_name
