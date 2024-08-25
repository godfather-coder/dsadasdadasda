from django.urls import path
from .views import  GetAllListings, DeleteAllListings, MyHomeListing, SSListing

urlpatterns = [

    path('myListings/', GetAllListings.as_view()),

    path('deleteListings/', DeleteAllListings.as_view()),


    path('uploadMyHomeListing/', MyHomeListing.as_view()),

    path('uploadSSListing/', SSListing.as_view()),



]
