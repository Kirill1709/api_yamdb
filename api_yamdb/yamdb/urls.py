from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, get_confirmation_code, get_token

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/email/', get_confirmation_code),
    path('v1/auth/token/', get_token,
         name='get_token')
]
