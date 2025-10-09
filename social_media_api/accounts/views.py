from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, SimpleUserSerializer, FollowSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token = Token.objects.get(user=user)
        return Response({'user': response.data, 'token': token.key})


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        target = get_object_or_404(User, pk=user_id)
        if request.user == target:
            return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target)
        return Response(SimpleUserSerializer(target, context={"request": request}).data, status=status.HTTP_200_OK)

class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        target = get_object_or_404(User, pk=user_id)
        if request.user == target:
            return Response({"detail": "Cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.unfollow(target)
        return Response({"detail": "unfollowed"}, status=status.HTTP_200_OK)

class FollowingListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SimpleUserSerializer
    pagination_class = None

    def get_queryset(self):
        return self.request.user.following.all()
