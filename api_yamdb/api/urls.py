from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUp

app_name = 'api'

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
]
