from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import MemberSerializer, TokenSerializer, LoginSerializer, MemberDetailSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

#  Create your views here.

class MemberViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MemberSerializer

    @action(detail=False, methods=['post'], url_path='tokens')
    def tokens(self, request):
        serializer = TokenSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access': access_token,
                'refresh': refresh_token,
            }, status = status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid Credentials'}, status= status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def token_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid()
        token = serializer.validated_data['token']

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
        except:
            try:
                refresh_token = RefreshToken(token)
                user_id = refresh_token['user_id']
            except Exception as e:
                raise AuthenticationFailed('Invalid Token.')
            
        try:
            user = User.objects.get(id= user_id)
        except:
            return Response({'detail': 'User not found.'})

        user_serializer = MemberDetailSerializer(user)

        return Response(user_serializer.data)


