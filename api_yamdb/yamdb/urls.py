from rest_framework.routers import DefaultRouter

from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView


from .views import CommentViewSet, ReviewViewSet, UserViewSet, get_confirmation_code, get_token

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

url_token = [
    path('token/', get_token,
         name='get_token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/email/', get_confirmation_code),
    path('v1/auth/token/', get_token,
         name='get_token')
]
