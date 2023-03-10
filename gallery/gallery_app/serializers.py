from rest_framework import serializers
from gallery_app.models import UserProfile, UserGallery


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class GalleryPostSerializer(serializers.ModelSerializer):

    # user = serializers.RelatedField(source='UserGallery', read_only=True)
    # image_post = serializers.RelatedField(source='UserGallery', allow_null=True)

    class Meta:
        model = UserGallery
        fields = ['id', 'user', 'image_post', 'video_post', 'caption']
        extra_kwargs = {
            'user': {'read_only': True},
            'image_post': {'allow_null': True},
            'video_post': {'allow_null': True},
            'caption': {'allow_null': True}
        }