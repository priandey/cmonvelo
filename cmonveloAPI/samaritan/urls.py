from django.urls import path

from .views import StolenBikes, CreateFoundAlert

urlpatterns = [
    path('stolen-bikes/', StolenBikes.as_view()),
    path('found/', CreateFoundAlert.as_view()),
]