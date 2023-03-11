from django.urls import path
from gallery_app import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register_view'),
    path('login/', views.LoginAPIView.as_view(), name='login_view'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout_view'),
    path('gallery/', views.GalleryPostAPIView.as_view(), name='gallery_view'),
    path('gallery/<int:pk>/', views.GalleryPostAPIView.as_view(), name='action_gallery_view'),
]
