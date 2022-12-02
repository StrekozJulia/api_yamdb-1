from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import ReceiveToken, SignUp

app_name = 'api'

urlpatterns = [
    path('v1/auth/token/', ReceiveToken.as_view(),
         name='token_obtain'),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
]
