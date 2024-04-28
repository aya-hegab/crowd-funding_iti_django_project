# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='accounts/images/', blank=True, null=True)

#     def __str__(self):
#         return self.user.username
    
    

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'
    

class AdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
    birthdate = models.DateField()
    country = models.CharField(max_length=20)
    facebook = models.URLField(max_length=200)


class ProfileActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Activation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return (timezone.now() - self.created_at).days >= 1