from django.contrib.auth import authenticate, login
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserSerializer


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            print(request.data)


            if serializer.is_valid():

                user = serializer.validated_data['user']
                tokens = get_tokens_for_user(user)  # Generate tokens for the user
                return Response(tokens, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"msg": 'Error'})


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
