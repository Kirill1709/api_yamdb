import random

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import IsAdminOrReadOnly, IsAutrhOrAdminOrModeratorOrReadOnly
from .serializer import (CategorySerializer, CommentSerializer,
                         GenreSerializer, ReviewSerializer,
                         TitleReadSerializer, TitleWriteSerializer,
                         TokenSerializer, UserEmailSerializer,
                         UserSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.GenericViewSet, CreateAPIView, DestroyAPIView,
                   ListAPIView, RetrieveAPIView, UpdateAPIView):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_object(self):
        obj = get_object_or_404(Title, pk=self.kwargs.get('pk'))
        return obj

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAutrhOrAdminOrModeratorOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(
            Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAutrhOrAdminOrModeratorOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id'])
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdminUser]

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = UserEmailSerializer(request.data)
    email = serializer.data['email']
    try:
        validate_email(email)
    except ValidationError:
        return Response(
            data={'message': 'Данные введены неверно'})
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(username=email, email=email)
    confirmation_code = random.randint(1000000000, 9999999999)
    user = User.objects.filter(email=email)
    user.update(confirmation_code=confirmation_code)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        'admin@yandex.ru',
        [email]
    )
    return Response(
        data={'message': f'Код выслан на email: {email}'}
    )


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(User, email=email)
    if confirmation_code != user.confirmation_code:
        return Response(
            data={'confirmation_code': 'Несоответствие кода подтверждения'})
    token = AccessToken.for_user(user)
    return Response({f'token: {token}'})
