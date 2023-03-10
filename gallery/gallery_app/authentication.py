import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.conf import settings
from django.contrib.auth import get_user_model


class SafeJWTAuthentication(BaseAuthentication):
    """Custom authentication for JWT"""

    def authenticate(self, request):
        print('cookies============', request.META.get('HTTP_AUTHORIZATION'))
        UserProfile = get_user_model()
        token = request.COOKIES.get('jwt', None)

        if not token:
            token = request.META.get('HTTP_AUTHORIZATION', None)
        print('token===================', token)
        if not token or token=='null':
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = UserProfile.objects.filter(id=payload['id']).first()

        if not user:
            raise AuthenticationFailed('Unauthenticated')
        
        return (user, None)
