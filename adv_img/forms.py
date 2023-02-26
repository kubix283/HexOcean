from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import MyImage


class ExperianImageForm(forms.ModelForm):
    expiration_time = forms.IntegerField(label='Expiration time (seconds)',
                                        validators=[MinValueValidator(300), 
                                                    MaxValueValidator(30000)])
    
    class Meta:
        model = MyImage
        fields = ['image']
        labels = {'image': 'Image'}