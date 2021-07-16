from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Category, Genre, Title
from .serializer import CategorySerializer, GenreSerializer, TitleSerializer, TitleListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if self.request.user.role == 'admin':
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDENT)

    def delete(self, request, pk):
        post = Category.objects.get(id=pk)
        if self.request.user.role == 'admin':
            serializer = CategorySerializer(post, data=request.data, partial=True)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if self.request.user.role == 'admin':
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDENT)

    def delete(self, request, pk):
        post = Category.objects.get(id=pk)
        if self.request.user.role == 'admin':
            serializer = CategorySerializer(post, data=request.data, partial=True)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ('get', 'post', 'delete', 'patch')
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if self.request.user.role == 'admin':
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDENT)

    def delete(self, request, pk):
        post = Category.objects.get(id=pk)
        if self.request.user.role == 'admin':
            serializer = CategorySerializer(post, data=request.data, partial=True)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDENT)

    def patch(self, request, pk):
        post = Category.objects.get(id=pk)
        if self.request.user.role == 'admin':
            serializer = CategorySerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDENT)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer
