from django import forms
from .models import Image
from django.core.exceptions import ValidationError


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)

    def clean_image(self):
        image = self.cleande_data.get('image')
        if image:
            if image.content_type != 'image/jpeg':
                raise ValidationError('Only JPEG files are allowed.')
            if image.size > 10 * 1024 * 1024:
                raise ValidationError('File size cannot exceed 10 MB.')
        return image
