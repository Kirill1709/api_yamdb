from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, get_confirmation_code, get_token

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

url_token = [
    path('token/', get_token,
         name='get_token'),
    
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/email/', get_confirmation_code),
    path('v1/auth/token/', get_token,
         name='get_token')
]
