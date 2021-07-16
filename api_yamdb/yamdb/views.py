from django.core.exceptions import ValidationError
from rest_framework import viewsets

from .models import User
from .serializer import UserSerializer, UserEmailSerializer, TokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import random
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken


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
        'admin@admin.com',
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
