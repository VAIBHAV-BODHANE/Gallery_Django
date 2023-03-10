from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from gallery_app.models import UserProfile, UserGallery
from gallery_app.serializers import UserProfileSerializer, GalleryPostSerializer
from datetime import datetime, timedelta as td
import jwt


class RegisterAPIView(APIView):
    """Register the user"""

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "User Created Successfully!", "status": 200}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """Login view"""

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = UserProfile.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() +  td(minutes=60),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        response.status_code = status.HTTP_200_OK
        
        return response


class LogoutAPIView(APIView):
    """Logout the authenticated user"""

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt',None)

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = UserProfile.objects.filter(id=payload['id']).first()

        if not user:
            raise AuthenticationFailed('Unauthenticated')
        
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Logout Successfully!", "status": 200
        }
        response.status_code = status.HTTP_200_OK

        return response


class GalleryPostAPIView(APIView):
    """Retrive and upload the images and videos"""

    def get(self, request, *args, **kwargs):


        token = request.COOKIES.get('jwt',None)

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = UserProfile.objects.filter(id=payload['id']).first()

        if not user:
            raise AuthenticationFailed('Unauthenticated')
        # print(request.user.email)

        qs = UserGallery.objects.all()
        serializer = GalleryPostSerializer(qs, many=True)
        return Response({"data": serializer.data, "status": 200}, status=status.HTTP_200_OK)