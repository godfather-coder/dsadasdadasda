from django.contrib.auth import authenticate, login
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, UserActionLog
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class TokenVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token', None)
        if token is None:
            return Response({"msg": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = AccessToken(token)

            # Check if the token matches the current token in the user model
            user = User.objects.get(id=decoded_token['user_id'])
            if str(decoded_token) != user.current_jwt_token:
                return Response({"msg": "Token is invalid or has been replaced"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"msg": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": "Token is invalid", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
class LoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']

                # Invalidate the old token (optional)
                if user.current_jwt_token:
                    try:
                        old_token = AccessToken(user.current_jwt_token)
                        old_token.blacklist()  # This requires the token to be blacklisted
                    except Exception as e:
                        print(f"Error invalidating old token: {e}")

                # Generate new tokens for the user
                tokens = get_tokens_for_user(user)

                # Save the new access token to the user
                user.current_jwt_token = tokens['access']
                user.save()

                return Response(tokens, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"msg": 'Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetLogsBySession(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request, session_id):
        # Retrieve all logs with the given session_id
        logs = UserActionLog.objects.filter(session_id=session_id)

        # Prepare data for response
        log_data = [{
            'session_id': "efw",
            'user': log.user.phone_number,
            'action': log.action,
            'details': log.details,
            'timestamp': log.timestamp
        } for log in logs]

        return Response({'session_id': session_id, 'logs': log_data}, status=200)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    # Store the access token in the user model
    user.current_jwt_token = str(access_token)
    user.save()

    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }