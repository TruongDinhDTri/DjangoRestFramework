from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

# from DjangoRestFramework.LearningDRF.BookApp import api

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        if len(data['username']) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        return data


@csrf_exempt
@api_view(['POST'])
def UserCreationApi(request):
    """
    API endpoint for user creation.
    """
    data = request.data
    username = data['username']
    password = data['password']
    
    user = User.objects.create_user(
        username=username,
        password=password
    )
    serializers = UserSerializer(user)
    return Response({
        "message": "User created successfully",
        "data": serializers.data
    }, status=201)
    
    
@api_view(['POST'])
def UserLoginApi(request):
    """
    API endpoint for user creation.
    """
    data = request.data
    username = data['username'],
    password = data['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        # login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        serializers = UserSerializer(user)
        return Response({
            "message": "User logged in successfully",
            'token': token.key,
            "data": serializers.data
        }, status=200)
    else:
        return Response({
            "message": "Invalid credentials"
        }, status=400)


@api_view(['GET'])
def UserListApi(request):
    """
    API endpoint for listing all users.
    """
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data, status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProtectedViewApi(request):
    """
    A protected view that requires authentication.
    """
    return Response({
            "message": f"Hello, {request.user.username}!"
    }, status=200)
