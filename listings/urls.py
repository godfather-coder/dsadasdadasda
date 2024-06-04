from django.urls import path
from .views import  GetAllListings, DeleteAllListings, SpecificListing

urlpatterns = [

    path('myListings/', GetAllListings.as_view()),

    path('deleteListings/', DeleteAllListings.as_view()),


    path('uploadSpecificListing/', SpecificListing.as_view()),



]
