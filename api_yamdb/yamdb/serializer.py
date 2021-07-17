from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')
        model = Title


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugField(source='author.username')
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, attrs):
        user = self.context['request'].user
        title = attrs['title']
        if self.context['request'].method == 'POST' and Review.objects.get(
                title_id=title, author=user).exists:
            raise serializers.ValidationError('Вы уже оставили рецензию!')
        return super().validate(attrs)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )
