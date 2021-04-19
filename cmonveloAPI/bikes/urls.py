from django.urls import path
from .views import RobbedBikesView, VerifyToken, BikeDetailView, FoundBikeView, TraitsView

urlpatterns = [
    path("", RobbedBikesView.as_view(), name="robbed_bikes"),
    path("pwl/verify/", VerifyToken, name="verify_token"),
    path("bike/<int:pk>/", BikeDetailView.as_view(), name="bike_detail"),
    path("bike/<int:pk>/found/", FoundBikeView.as_view(), name="bike_found"),
    path("traits/", TraitsView.as_view(), name="traits"),
]