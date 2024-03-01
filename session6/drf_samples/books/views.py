from django.http import JsonResponse, HttpRequest
# Create your views here.
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book, Comment, Company
from books.serializers import BookSerializer, CommentSerializer, CompanySerializer


class BookView(View):
    def get(self, request: HttpRequest):
        return JsonResponse({'name': None}, safe=False)


# class CommentListView(APIView):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()
#
#     def get_queryset(self):
#         return self.queryset
#
#     def get_serializer(self):
#         return self.serializer_class(self.get_queryset(), many=True, context={'request': self.request})
#
#     def get(self, request):
#         serializer = self.get_serializer()
#         return Response(serializer.data)

class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tag', 'user']
    search_fields = ['^tag', 'text']


class BookApiView(CreateModelMixin, RetrieveUpdateAPIView):
    """
    My Book API view
    """
    queryset = Book.objects.filter(published_date__gt='2020-01-01')
    serializer_class = BookSerializer

    # def filter_queryset(self, queryset):
    #     return queryset.filter(title=self.request.query_params.get('text'))
    # def post(self, request, *args, **kwargs):
    #     book_serializer = BookSerializer(data=request.data)
    #     book_serializer.is_valid(raise_exception=True)
    #     book = book_serializer.save(something=True)
    #     print('request data was valid', book_serializer.validated_data['title'])
    #     return Response(book_serializer.data)


class BookViewset(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['publish', 'archive', 'published_date', ]
    search_fields = ['=title', '@description', '$author__username']

    @action(detail=True, url_path='pub', methods=['GET', 'POST'])
    def publish(self, request, pk):
        return Response({'message': 'published'})

    @action(detail=True, methods=['GET', 'POST'])
    def archive(self, request, pk):
        return Response({'message': 'archived'})

    @action(detail=True, permission_classes=[IsAuthenticated], methods=['POST'])
    def submit_comment(self, request, pk):
        book = self.get_object()
        comment = Comment.objects.create(text=request.data.get('text'), user=request.user, book=book)
        return Response(CommentSerializer(comment, context={'request': request}).data)

    @submit_comment.mapping.delete
    def delete_comment(self, request, pk):
        Comment.objects.get(pk=self.kwargs.get('pk')).delete()
        return Response({"message": "deleted"})


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [
        TokenAuthentication, JWTAuthentication
    ]
    permission_classes = [IsAuthenticated]


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(f'token was generated: {token}')
        return Response({'token': token.key})


# class CustomObtainPairView(TokenObtainPairView):
#     serializer_class = CustomObtainTokenSerializer
