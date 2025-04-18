from django.contrib.auth import authenticate
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializer import UserRegisterSerializer, UserModelSerializer, LoginSerializer


@extend_schema(tags=['auth'], request=UserRegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data
    serializer = UserRegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(UserModelSerializer(instance=serializer.instance).data)
    return Response(serializer.errors)


@extend_schema(tags=['auth'], request=LoginSerializer)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        return Response(serializer.errors)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        })
