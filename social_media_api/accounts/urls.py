from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowAPIView, UnfollowAPIView, FollowingListAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowAPIView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowAPIView.as_view(), name='unfollow'),
    path('following/', FollowingListAPIView.as_view(), name='following-list'),
]
