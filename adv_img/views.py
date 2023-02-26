from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExperianImageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .models import MyImage




@login_required
def add_image(request):
    if request.method == 'POST':
        form = ExperianImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.upload_time = timezone.now()
            image.save()
            return redirect('image_detail', pk=image.pk)

    else:
        form = ExperianImageForm()
    return render(request, 'adv/add_image.html', {'form': form})


class ImageDetailView(LoginRequiredMixin, DetailView):
    model = MyImage
    template_name = 'adv/image_detail.html'
    context_object_name = 'image'
    

    # def get_object(self, queryset=None):
    #     obj = get_object_or_404(self.model, id=self.kwargs['pk'],
    #                              user__user=self.request.user.myprofile)
    #     return obj

