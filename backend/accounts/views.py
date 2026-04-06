from rest_framework import status
from rest_framework.decoratos import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAutheicated
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefereshToken
from django.contrib.auth import authenticate 
from .models import Profile

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    ProfileSerializers, 
    AddressSerializers, 
    UserSeralizer
)

from .services import AccountServices

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        user = AccountServices.create_user(
            email = serializer.validate_data["email"], 
            password = serializer.validated_data['password'], 
            phone = serializer.vlaidated_data["phone"]
        )

        refresh = RefereshToken.for_user(user)

        return Response(
            {
                "user": UserSeralizer(user).data,
                "tokens": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
            }, 
            status = status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data = request.data)
    if serializer.is_valid():
        user = authenticate(
            email = serializer.validated_data["email"],
            password = serializer.validated_data["password"],
        )

        if user:
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "user": UserSeralizer(user).data,
                    "tokens": {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                }, 
                status = status.HTTP_201_CREATED, 
            )
        return Response({"error": "Invalid credentials"}, status = status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    profile_obj = Profile.objects.get(user = request.user)

    if request.method == 'GET':
        seralizer = ProfileSerializers(profile_obj, context = {
            'request': request})
        return Response(seralizer.data)
    elif request.method == 'PATCH':
        seralizer = ProfileSerializers(profile_obj, data = request.data, partial = True, context = {'request': request})
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_fcm_token(request):
    fcm_token = request.data.get("fcm_token")

    if not fcm_token:
        return Response(
            {'error': 'fcm_token is required'}, status = status.HTTP_400_BAD_REQUEST
        )
    AccountServices.update_fcm_token(request.user, fcm_token)
    return Response({"message": "FCM token updated successfully"})

@api_view(["GET", "POST"])
@permission_classes([IsAutheicated])
def addresses(request):
    if request.method == 'GET':
        addresses = AccountServices.get_user_addresses(request.user)
        return Response(AddressSerializers(addresses, many = True).data)
    elif request.method == 'POST':
        seralizer = AddressSerializers(data = request.data)

        if serializer.is_valid():
            address = AccountServices.create_address(
                request.user, **serializer.validated_data
            )

            return Response(
                AddressSerializers(address).data, status=status.HTTP_200_CREATED
            )
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAutheicated])
def address_detail(request, address_id):
    try:
        if request.method == 'GET':
            address = AccountServices.get_address(request.user)
            return Response(AddressSerializers(addresses, many = True).data)
        elif request.method in ['PUT','PATCH']:
            serializer = AddressSerializers(data = request.data, partial = (request.method == 'PATCH'))

            if serializer.is_valid():
                address = AccountServices.update_address(request.user, address_id, **serializer.validated_data)
                return Response(AddressSerializers(address).data)
            
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

