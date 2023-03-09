from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class SimpleAPIView(APIView):
    """Simple View for test"""

    def get(self, request, *args, **kwargs):
        return Response({"msg": "success"}, status=status.HTTP_200_OK)
