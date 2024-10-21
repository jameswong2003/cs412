from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
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
