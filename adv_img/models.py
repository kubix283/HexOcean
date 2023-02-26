from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from PIL import Image as PILImage
from io import BytesIO
from django.utils import timezone
from datetime import timedelta
from django.core.files.base import ContentFile



class Thumbnail(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    description = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f'{self.width}x{self.height} ({self.description})'
    

class Tier(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ManyToManyField(Thumbnail, blank=True)
    link_to_original = models.BooleanField(default=False)
    expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    

class MyImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images_v2', null=True, blank=True)
    thumbnail = models.ManyToManyField(Thumbnail, blank=True)
    link_to_original = models.BooleanField(default=False)
    thumbnail_200 = models.ImageField(upload_to='images_v2/thumbnails/200/', null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to='images_v2/thumbnails/400/', null=True, blank=True)
    expiring_links = models.BooleanField(default=False)
    expiration_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Create appropriate thumbnails for the user's tier
        if self.image and not self.thumbnail_200:
            self.create_thumbnail_200()
        if self.image and not self.thumbnail_400 and self.user in ['premium', 'enterprise']:
            self.create_thumbnail_400()
        # if self.image and not self.thumbnail_400 and self.user.tier == 'enterprise':
        #     self.create_thumbnail()
        if self.image and self.user == 'enterprise':
            self.expiring_links = True
            for thumbnail in self.user.tier.thumbnails.all():
                width, height = thumbnail.width, thumbnail.height
                thumbnail_name = f'thumbnail_{width}x{height}'
                if self.image and not hasattr(self, thumbnail_name):
                    self.create_thumbnail(thumbnail, thumbnail_name)
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


    # def save(self, *args, **kwargs):
    #     for thumbnail in self.user.tier.thumbnails.all():
    #         width, height = thumbnail.width, thumbnail.height
    #         thumbnail_name = f'thumbnail_{width}x{height}'
    #         if self.image and not hasattr(self, thumbnail_name):
    #             self.create_thumbnail(thumbnail, thumbnail_name)

    #     super().save(*args, **kwargs)


    def create_thumbnail(self, thumbnail, thumbnail_name):
        im = PILImage.open(self.image)
        output_size = (thumbnail.width, thumbnail.height)
        im.thumbnail(output_size)
        # thumbnail_io = BytesIO()
        # im.save(thumbnail_io, 'JPEG', quality=85)
        field = models.ImageField(upload_to=f'images_v2/thumbnails/{thumbnail_name}/', null=True, blank=True)
        setattr(self, thumbnail_name, field)
        field.save(self.image.name)

    def get_image_url(self):
        if self.expiring_links:
            return self.image.url + f'?expires={int(timezone.now().timestamp() + self.expiration_time)}'
        else:
            return self.image.url
        
