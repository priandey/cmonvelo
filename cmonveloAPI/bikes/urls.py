from django.urls import path
from .views import RobbedBikesView, VerifyToken, BikeDetailView, FoundBikeView, TraitsView, AskModeration, ModerateBike

urlpatterns = [
    path("", RobbedBikesView.as_view(), name="robbed_bikes"),
    path("ask_moderation/", AskModeration, name="ask_moderation"),
    path("moderate/<int:pk>/<str:token>/", ModerateBike, name="moderate_bike"),
    path("pwl/verify/", VerifyToken, name="verify_token"),
    path("bike/<int:pk>/", BikeDetailView.as_view(), name="bike_detail"),
    path("bike/<int:pk>/found/", FoundBikeView.as_view(), name="bike_found"),
    path("traits/", TraitsView.as_view(), name="traits"),
]