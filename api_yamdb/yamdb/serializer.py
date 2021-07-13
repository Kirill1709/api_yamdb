from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.fields import CurrentUserDefault

from .models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'pub_date', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugField(source='author.username')
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, attrs):
        user = self.context['request'].user
        title = attrs['title']
        if self.context['request'].method == 'POST' and Review.objects.get(title=title, author=user).exists:
            raise serializers.ValidationError('Вы уже оставили рецензию!')
        return super().validate(attrs)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'pub_date', 'author', 'overall_rating_field', )
