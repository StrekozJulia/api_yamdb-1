from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ReceiveToken,
                    SignUp,
                    TitleViewSet,
                    GenreViewSet,
                    CategoryViewSet
                    )

app_name = 'api'

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/token/', ReceiveToken.as_view(), name='token_obtain'),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/', include(router.urls))
]
