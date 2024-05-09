
from django.urls import path
from views import ObtainToken

urlpatterns = [
    path('api/token/', ObtainToken.as_view(), name='obtain_token'),
]
