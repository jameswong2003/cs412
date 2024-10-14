from django.db import models
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')


class StatusMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"Status by {self.profile.first_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {self.message[:20]}..."