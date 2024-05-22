from django.urls import path
from .views import LoginView, UserRegistrationAPIView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', UserRegistrationAPIView.as_view()),

]
