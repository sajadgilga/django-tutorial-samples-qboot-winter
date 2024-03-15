import random
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
# Create your tests here.
from django.urls import reverse
from model_bakery import baker, seq
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from books.models import Book, Comment
from books.views import check_scripts, CommentView

User = get_user_model()


class BookCreateTestCase(TestCase):
    def setUp(self):
        self.books = [Book.objects.create(title=f'test {i}', description=f'description {i}', tags='') for i in
                      range(100)]

    def tearDown(self):
        pass

    def test_check_scripts(self):
        text = 'safe text'
        result = check_scripts(text)
        self.assertEqual(result, text)

    def test_check_scripts_with_xss_input(self):
        text = '<script>alert("xss")</script>'
        with self.assertRaises(ValidationError):
            result = check_scripts(text)

    @tag('success')
    @patch('books.serializers.get_data_from_external_service')
    def test_book_list_view(self, mock_obj):
        mock_obj.return_value = 'my desired value'
        # mock_obj.side_effect = Exception('some exception')
        response = self.client.get(reverse('book-list-api'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('count' in response.data)
        self.assertEqual(response.data.get('count'), 100)
        self.assertEqual(response.data.get('total_pages'), 3)
        self.assertEqual(response.data['results'][0]['title'], 'test 0')
        self.assertEqual('my desired value', response.data['results'][0]['external_data'])
        mock_obj.assert_any_call('test 4')

    def test_book_list_with_pagination(self):
        response = self.client.get(reverse('book-list-api') + '?page=2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['current_page'], 2)

    def test_book_list_template_view(self):
        response = self.client.get(reverse('book-list-view'))

        self.assertTemplateUsed(response, 'book-list.html')


class AuthTestCase(TestCase):
    def setUp(self):
        self.username, self.password = 'test_user', 'test_pass'
        User.objects.create_user(username=self.username, password=self.password)

    @tag('success')
    def test_obtain_token_success(self):
        response = self.client.post(reverse('obtain-token'), data={
            'username': self.username, 'password': self.password
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)

    @tag('failure')
    def test_obtain_token_wrong_password_failure(self):
        response = self.client.post(reverse('obtain-token'), data={
            'username': self.username, 'password': 'wrong password'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'].code, 'no_active_account')

    @tag('failure')
    def test_obtain_token_wrong_username_failure(self):
        response = self.client.post(reverse('obtain-token'), data={
            'username': 'wrong username', 'password': 'wrong password'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'].code, 'no_active_account')

    @tag('failure')
    def test_obtain_token_wrong_format_failure(self):
        response = self.client.post(reverse('obtain-token'), data={
            'email': 'wrong username'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)


def mock_get_data():
    print('mock get data called!')
    return 'mock data'


class CommentTestCase(APITestCase):
    def setUp(self):
        self.books = baker.make('books.Book', 10, title=seq('book '))
        self.username, self.password = 'test_user', 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.comments = baker.make('books.Comment', 100, user=self.user, book=lambda: random.choice(self.books))

    @patch('books.serializers.get_data_from_external_service', mock_get_data)
    def test_comment_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('comment-create-list-view'))
        force_authenticate(request, self.user)
        view = CommentView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['external_data'], 'mock data')

    def test_create_comment(self):
        login_response = self.client.post(reverse('obtain-token'), data={
            'username': self.username, 'password': self.password
        }, format='json')
        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        comment_text = 'test comment'
        response = self.client.post(reverse('comment-create-list-view'), data={
            'text': comment_text, 'book': self.books[0].id, 'user': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Comment.objects.filter(text=comment_text).exists())

    def test_get_comment_list_with_cache(self):
        with self.modify_settings(MIDDLEWARE={
            'append': 'django.middleware.cache.FetchFromCacheMiddleware',
            'prepend': 'django.middleware.cache.UpdateCacheMiddleware',
        }):
            login_response = self.client.post(reverse('obtain-token'), data={
                'username': self.username, 'password': self.password
            }, format='json')
            token = login_response.data['access']

            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

            response = self.client.get(reverse('comment-create-list-view'))

            cache_key = 'something'
            self.assertIsNotNone(cache.get(cache_key))

# class SampleBookTestCase(SimpleTestCase):
#     def test_book_list_view(self):
#         Book.objects.create(title='test', description='test', tags='')
