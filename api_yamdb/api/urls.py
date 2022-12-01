from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReceiveToken, SignUp, UsersViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UsersViewSet, )

urlpatterns = [
    path('v1/auth/token/', ReceiveToken.as_view(),
         name='token_obtain'),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),
]
