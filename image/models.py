from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile

class Profile(models.Model):
    TIERS = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.CharField(max_length=10, choices=TIERS, 
                            default='basic', blank=True, 
                            null=True)


    def __str__(self):
        return self.user.username

class Image(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail_200 = models.ImageField(upload_to='images/thumbnails/200/', null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to='images/thumbnails/400/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Create appropriate thumbnails for the user's tier
        if self.image and not self.thumbnail_200:
            self.create_thumbnail_200()
        if self.image and not self.thumbnail_400 and self.user.tier in ['premium', 'enterprise']:
            self.create_thumbnail_400()
            self.create_thumbnail_200()
        super().save(*args, **kwargs)

    def create_thumbnail_200(self):
        im = PILImage.open(self.image)
        output_size = (200, 200)
        im.thumbnail(output_size)
        thumbnail_io = BytesIO()
        im.save(thumbnail_io, 'JPEG', quality=85)
        thumbnail_io.seek(0)
        self.thumbnail_200.save(self.image.name, ContentFile(thumbnail_io.read()), save=False)

    def create_thumbnail_400(self):
        im = PILImage.open(self.image)
        output_size = (400, 400)
        im.thumbnail(output_size)
        thumbnail_io = BytesIO()
        im.save(thumbnail_io, 'JPEG', quality=85)
        thumbnail_io.seek(0)
        self.thumbnail_400.save(self.image.name, ContentFile(thumbnail_io.read()), save=False)

    def __str__(self):
        return self.image.name


