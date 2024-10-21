from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm

# Create your views here.

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # Retrieve the profile associated with this status message
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile

        # Save the form and get the StatusMessage instance
        sm = form.save()

        # Retrieve the uploaded files from the form data
        files = self.request.FILES.getlist('files')

        # Process each file and create Image objects
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()  # Save each image to the database

        return super().form_valid(form)

    def get_success_url(self):
        profile_pk = self.kwargs['pk']
        return reverse_lazy('show_profile', kwargs={'pk': profile_pk})
