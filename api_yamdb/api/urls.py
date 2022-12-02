from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (ReceiveToken,
                    SignUp,
                    TitleViewSet,
                    GenreViewSet,
                    CategoryViewSet
                    )

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/token/', ReceiveToken.as_view(),
         name='token_obtain'),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/', include(router_v1.urls))
]
