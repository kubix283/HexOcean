from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Image, Profile
from .forms import ImageForm
from django.views.generic import TemplateView, ListView


class HomeView(TemplateView):
    template_name = 'index.html'

def user_images(request):
    user_images = Image.objects.all().filter(user=request.user.profile)
    return render(request, 'image_list.html', {'user_images': user_images})


def add_image(request):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            image = form.save(commit=False)
            image.user = profile
            image.save()
            return redirect('images')
        
    else:
        form = ImageForm()
    return render(request, 'add_image.html', {'form': form})


def profile_detail(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'profile.html', context={profile: profile})