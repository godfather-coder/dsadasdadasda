from django.urls import path
from .views import LoginView, UserRegistrationAPIView, TokenVerifyView, GetLogsBySession

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', UserRegistrationAPIView.as_view()),
    path('verifyToken/', TokenVerifyView.as_view()),
    path('logs/session/<uuid:session_id>/', GetLogsBySession.as_view(), name='get_logs_by_session'),

]
