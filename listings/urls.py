from django.urls import path
from .views import StartBotApi, GetAllListings, DeleteAllListings, GetBotStatus, EndBot, SpecificListing

urlpatterns = [
    path('startbot/', StartBotApi.as_view()),

    path('myListings/', GetAllListings.as_view()),

    path('deleteListings/', DeleteAllListings.as_view()),

    path('GetBotStatus/', GetBotStatus.as_view()),

    path('EndBot/', EndBot.as_view()),

    path('uploadSpecificListing/', SpecificListing.as_view()),



]
