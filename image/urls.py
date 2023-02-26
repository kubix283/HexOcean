from django.urls import path
from image import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('image/add/', views.add_image, name='add_image'),
    path('images/', views.user_images, name='images'),
    path('profile/', views.profile_detail, name='profile')
]