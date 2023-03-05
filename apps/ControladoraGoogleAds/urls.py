from django.urls import path

from .views import *

urlpatterns = [
    path('list_ads', ControladoraGoogleAds.as_view())
]