from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated

from gallery_app.models import UserProfile, UserGallery
from gallery_app.serializers import UserProfileSerializer, GalleryPostSerializer
from gallery_app.authentication import SafeJWTAuthentication
from gallery_app.permissions import OwnObjectPermission

from datetime import datetime, timedelta as td
import jwt


class RegisterAPIView(APIView):
    """Register the user"""
    
    permission_classes=[AllowAny,]
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "User Created Successfully!", "status": 200}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """Login view"""

    permission_classes=[AllowAny,]

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

    authentication_classes = [SafeJWTAuthentication,]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Logout Successfully!", "status": 200
        }
        response.status_code = status.HTTP_200_OK

        return response


class GalleryPostAPIView(APIView):
    """Retrive and upload the images and videos"""

    authentication_classes = [SafeJWTAuthentication]
    permission_classes = ([OwnObjectPermission])
    serializer_class = GalleryPostSerializer

    def get_object(self, pk):
        try:
            return UserGallery.objects.get(id=pk)
        except UserGallery.DoesNotExist:
            return status.HTTP_404_NOT_FOUND 
        return super().get_object()

    def get(self, request, *args, **kwargs):
        qs = UserGallery.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response({"data": serializer.data, "status": 200}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({"message": "Successfully uploaded!", "status": 201}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk, *args, **kwargs):
        qs = self.get_object(pk)
        if qs != 404:
            self.check_object_permissions(request, qs)
            qs.delete()
            return Response({"message": "Post deleted!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Post does not exist!"}, status=status.HTTP_404_NOT_FOUND)




