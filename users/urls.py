from django.urls import path
from .views import LoginView, UserRegistrationAPIView,TokenVerifyView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', UserRegistrationAPIView.as_view()),
    path('verifyToken/', TokenVerifyView.as_view()),

]
