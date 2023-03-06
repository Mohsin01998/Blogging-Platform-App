
from django.contrib.auth.models import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # fields for user model
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email_token=models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
