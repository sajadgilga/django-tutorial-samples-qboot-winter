from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from books.models import Book, Comment, Company, Department


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
    id = serializers.IntegerField()
    text = serializers.CharField()
    user_id = serializers.IntegerField(write_only=True)

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=True, validators=[check_min_length])
    description = serializers.CharField()
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    id = serializers.IntegerField(read_only=True)
    info = serializers.CharField(read_only=True)
    published_date = serializers.DateField(allow_null=True, required=False, initial='2022-10-10')
    comments = CommentLeanSerializer(many=True)

    # def get_comments(self, obj):
    #     # any desired logic
    #     return CommentLeanSerializer(obj.comments, many=True).data

    def validate_title(self, value):
        # check_unique_title(value)
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
        comments = validated_data['comments']
        instance.title = validated_data['title']
        if 'author_id' in validated_data:
            instance.author_id = validated_data['author_id']
        instance.published_date = validated_data['published_date']
        instance.description = validated_data['description']
        instance.save()
        for comment in comments:
            Comment.objects.filter(id=comment['id']).update(**comment)
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
    book = HyperlinkedRelatedField(view_name="book-detail", read_only=True)
    user_name = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['book', 'text', 'id', 'user', 'user_name', 'tag']
        extra_kwargs = {'text': {'required': False}}
        depth = 1

    def get_user_name(self, obj: Comment):
        return obj.user.first_name + ' ' + obj.user.last_name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class DepartmentSerializer(serializers.ModelSerializer):
    director = UserSerializer()
    members = UserSerializer(many=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'director', 'members']

    def update(self, instance, validated_data):
        members = validated_data.pop('members')
        director = validated_data.pop('director')
        department = super().update(instance, validated_data)
        for member_data in members:
            try:
                member = department.members.get(id=member_data.pop('id'))
            except User.DoesNotExist:
                raise ValidationError('user with this id not found')
            user_serializer = UserSerializer(member, member_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()


class CompanySerializer(serializers.ModelSerializer):
    date_type1 = serializers.SerializerMethodField(read_only=True)
    date_type2 = serializers.DateField(source='date', read_only=True)
    departments = DepartmentSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'owner',
            'size', 'field',
            'departments',
            'date_type1',  # first way to use different dates
            'date_type2',  # second way to use different dates
            'created_date', 'end_date'  # third way to use different dates
        ]

    def get_date_type1(self, obj):
        if obj.is_active:
            return obj.created_date
        return obj.end_date

    def to_representation(self, instance):
        result = super().to_representation(instance)
        if instance.is_active:
            result.pop('end_date')
        else:
            result.pop('created_date')
        return result

    def update(self, instance, validated_data):
        owner = validated_data.pop('owner')
        owner = self.context.get('request').user
        departments = validated_data.pop('departments')
        company = super().update(instance, validated_data)
        if 'id' not in owner:
            user = User.objects.create(**owner)
        else:
            try:
                user = User.objects.get(id=owner['id'])
            except User.DoesNotExist:
                raise ValidationError('no user with this id found')
            for key, value in owner.items():
                if key != 'id':
                    user.__setattr__(key, value)
            user.save()
        company.owner = user

        for department_data in departments:
            department = company.departments.filter(id=department_data.pop('id')).first()
            if not department:
                raise ValidationError('no department with this id found')

            # first way to update
            for key, value in department_data.items():
                if key != 'id':
                    setattr(department, key, value)
            department.save()

            # second way to update
            department_serializer = DepartmentSerializer(data=department_data, instance=department)
            department_serializer.is_valid(raise_exception=True)
            department_serializer.save()


class CustomObtainTokenSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        payload = super().get_token(user)
        payload['new_variable'] = 'hello world'
        payload['username'] = user.username
        return payload
