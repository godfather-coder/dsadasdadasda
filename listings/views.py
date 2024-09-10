from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .customs.logCreator import log_user_action
from .customs.main import upload
from .customs.ss.main import UploadOnSS
from .models import Listing

import uuid


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


class MyHomeListing(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            listing_data = request.data
            token = listing_data.get('token')
            urls = listing_data.get('url')
            sstoken = listing_data.get('sstoken')
            session_id = uuid.uuid4()

            log_user_action(user, 'დაიწყო ლისტინგის დადება', details=f'Token: {token}, URLs: {urls}, Session ID: {session_id}', session_id=session_id)

            if not sstoken:
                sstoken = None
            if not token:
                return Response({'error': 'შეიყვანე ტოკენი'}, status=402)
            if not urls:
                return Response({'error': 'შეიყვანე აიდი'}, status=402)

            urls = urls.split(',')

            for url in urls:
                url = url.strip()
                if Listing.objects.filter(listing_id=url, users=user).exists():
                    return Response({"msg": f"განცხადება {url} აიდით უკვე დევს"}, status=400)

            result = upload(urls, token, user, sstoken, session_id)

            log_user_action(user, 'Completed listing upload', details=f'Uploaded URLs: {urls}, Session ID: {session_id}', session_id=session_id)

            return Response({'message': result}, status=200)

        except Exception as e:
            return Response({'message': 'Something went wrong.'}, status=400)


class SSListing(APIView):
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

            for url in urls:
                url = url.strip()
                if Listing.objects.filter(listing_id=url, users=user).exists():
                    return Response({"msg": f"განცხადება {url} აიდით უკვე დევს"}, status=400)

            result = UploadOnSS(urls, token, user)

            return Response({'message': result}, status=200)

        except Exception as e:
            return Response({'message': 'Something went wrong.'}, status=400)
