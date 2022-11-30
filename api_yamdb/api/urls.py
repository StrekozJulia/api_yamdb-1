from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (TitleViewSet,
                    GenreViewSet,
                    CategoryViewSet
                    )

router = DefaultRouter()

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router.urls))
]