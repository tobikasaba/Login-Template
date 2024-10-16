from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):
    # creating a one-to-one relationship with the inbuilt User model.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fields
    portfolio_site = models.URLField(blank=True)
    # requires the pillow library installed
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username