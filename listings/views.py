import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import re
# from .customs.getListings import startBot
# from .customs.getInsideData import scrape_property_info
from .customs.main import upload
from .models import Listing
# from .customs.addListing import upload_listing_for_sale
#
# class StartBotApi(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#
#         try:
#             user = request.user
#             listing_data = request.data
#             token = listing_data.get('token')
#
#             if not token:
#                 return Response({'error': 'შეიყვანე ტოკენი'}, status=402)
#             if user.botStatus is True:
#                 return Response({'message': 'Bot is already running.'}, status=400)
#             user.botStatus = True
#             user.save()
#             startBot(token, user)
#             return Response({'message': 'Bot is running.'}, status=200)
#         except Exception as e:
#             print(e)
#             return Response({'message': 'Something went wrong.'}, status=400)
#
# class EndBot(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user = request.user
#         user.botStatus = False
#         user.save()
#
#         return Response({'message': 'ბოტი გამოირთო'}, status=201)
#
#
# class GetBotStatus(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         user = request.user
#
#         return Response(data={'status': user.botStatus}, status=200)


class GetAllListings(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        user_listings = Listing.objects.filter(users=user)

        if not user_listings.exists():
            return Response({'message': '0 განცხადება'}, status=200)

        listings_data = [{'listing_id': listing.listing_id} for listing in user_listings]
        listings_count = user_listings.count()

        return Response({
            'quantity': listings_count,
            'listings': listings_data
        }, status=200)


class DeleteAllListings(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        # Retrieve all listings associated with the authenticated user
        user_listings = Listing.objects.filter(users=user)

        # Check if the user has any listings
        if not user_listings.exists():
            return Response({'message': 'No listings found for the user'}, status=404)

        # Delete all listings associated with the user
        user_listings.delete()

        return Response({'message': 'All listings deleted successfully'}, status=200)

class SpecificListing(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            listing_data = request.data
            token = listing_data.get('token')
            urls = listing_data.get('url')

            if not token:
                return Response({'error': 'შეიყვანე ტოკენი'}, status=402)

            if not urls:
                return Response({'error': 'შეიყვანე აიდი'}, status=402)

            urls = urls.split(',')

            print(urls)

            for url in urls:
                url = url.strip()
                if Listing.objects.filter(listing_id=url, users=user).exists():
                    return Response({"msg": f"განცხადება {url} აიდით უკვე დევს"}, status=400)

            upload(urls, token)

            return Response({'message': 'ყველა განცხადება აიტვირთა!'}, status=200)

        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong.'}, status=400)