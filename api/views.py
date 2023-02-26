from rest_framework import generics
from rest_framework import permissions
from image.models import Image
from .serializers import ImageSerializer
from .mixins import IsStaffEditorPermission




class ImageListCreateAPIView(IsStaffEditorPermission, generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        image = serializer.validated_data.get('image')
        serializer.save(image=image)






class ImageDetailAPIView(IsStaffEditorPermission, generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageUpdateAPIView(IsStaffEditorPermission, generics.UpdateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'pk'

    def perform_update(self,serializer):
        super().perform_update(serializer)


class ImageDestroyAPIView(IsStaffEditorPermission, generics.DestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'pk'

    def perform_destroy(self,serializer):
        super().perform_destroy(serializer)


