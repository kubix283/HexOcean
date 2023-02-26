from django.urls import path
from . import views

urlpatterns = [
    path('add-image/', views.add_image, name='add-image'),
    path('image-detail/<int:pk>', views.ImageDetailView.as_view(), name='image_detail'),
]