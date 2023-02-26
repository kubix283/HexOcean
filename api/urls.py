from django.urls import path
from . import views


urlpatterns = [
    path('', views.ImageListCreateAPIView.as_view(), name='api'),
    path('<int:pk>/', views.ImageDetailAPIView.as_view()),
    path('<int:pk>/delete/', views.ImageDestroyAPIView.as_view()),
    path('<int:pk>/update/', views.ImageUpdateAPIView.as_view()),

]