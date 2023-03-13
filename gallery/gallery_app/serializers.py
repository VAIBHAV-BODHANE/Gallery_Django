from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from gallery_app.models import UserProfile, UserGallery

from datetime import datetime
from PIL import Image
import time, io, base64


def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None

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
    # video_post = serializers.RelatedField(source='UserGallery', allow_null=True)
    # post_caption = serializers.RelatedField(source='UserGallery', allow_null=True)

    created_by = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = UserGallery
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'image_post': {'allow_null': True},
            'video_post': {'allow_null': True},
            'post_caption': {'allow_null': True}
        }
    
    # def create(self, validated_data):
    #     request = self.context['request']
    #     print(request.data.get('base_code', None))
    #     image_bs = request.data.get('base_code', None)
    #     image_bs = image_bs.split(';base64',None)
    #     curr_time = time.mktime(datetime.now().timetuple())
    #     if image_bs:
    #         image_name = request.data.get('image_name', str(int(curr_time)))
    #         img = decodeDesignImage(image_bs)
    #         img_io = io.BytesIO()
    #         img.save(img_io, format='JPEG')
    #         f_img = InMemoryUploadedFile(img_io, field_name=None, name=image_name, content_type='image/jpeg', size=img_io.tell, charset=None)
    #         post = UserGallery.objects.create(
    #             post_caption=validated_data.get('post_caption'),
    #             image_post=f_img,
    #             user=request.user,
    #         )

    #         return post
    #     else:
    #         post = UserGallery.objects.create(
    #             post_caption=validated_data.get('post_caption'),
    #             video_post=validated_data.get('video_post'),
    #             user=request.user,
    #         )
    #         return post

    def get_created_by(self, obj):
        return obj.user.name
    
    def get_created(sefl, obj):
        return obj.created.astimezone(tz=settings.LOCAL_TIME_ZONE).strftime("%d-%m-%Y %H:%M:%S")
