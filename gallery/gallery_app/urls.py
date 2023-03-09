from django.urls import path
from gallery_app import views

urlpatterns = [
    path('', views.SimpleAPIView.as_view(), name='simple_view')
]
