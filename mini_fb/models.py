from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_friends(self):
        # Find all Friend instances where this Profile is either profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        # Collect the other profile in each Friend relation
        friends_profiles = [
            friend.profile2 for friend in friends_as_profile1
        ] + [
            friend.profile1 for friend in friends_as_profile2
        ]

        return friends_profiles
    
    def get_friend_suggestions(self):
        # Get the current friends of this profile
        current_friends = self.get_friends()
        
        # Exclude the current profile and the current friends
        suggested_profiles = Profile.objects.exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in current_friends])

        return suggested_profiles
    
    def add_friend(self, other):
        # Prevent self-friending
        if self == other:
            return

        # Check if a friendship already exists in either direction
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        # If no friendship exists, create a new one
        if not existing_friendship:
            Friend.objects.create(profile1=self, profile2=other)

class StatusMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"Status by {self.profile.first_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {self.message[:20]}..."
    
    def get_images(self):
        return self.images.all()
    
class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(default=timezone.now)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.status_message.profile.first_name}'s status at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friends_as_profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friends_as_profile2")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"