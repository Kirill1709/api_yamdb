from rest_framework import serializers

from .models import Comment, Review

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(max_length=10)

    
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
