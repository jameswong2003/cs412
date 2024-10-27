from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

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

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        profile_pk = self.kwargs['pk']
        return reverse_lazy('show_profile', kwargs={'pk': profile_pk})
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Get the profile associated with the StatusMessage
        status_message = self.get_object()
        profile_pk = status_message.profile.pk
        
        # Redirect to the profile page after deletion
        return reverse_lazy('show_profile', kwargs={'pk': profile_pk})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # After updating, redirect back to the profile page of the user who owns the status message
        status_message = self.get_object()
        profile_pk = status_message.profile.pk
        return reverse_lazy('show_profile', kwargs={'pk': profile_pk})

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # Extract the profile IDs from the URL parameters
        pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')

        # Retrieve the Profile instances
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)

        # Add the friend relationship
        profile.add_friend(other_profile)

        # Redirect back to the profile page
        return redirect('show_profile', pk=pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context