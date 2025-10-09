from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username
    
    def follow(self, user):
         # follow
        if user and user != self:
            self.following.add(user)

    def unfollow(self, user):
         # unfollow
        if user and user != self:
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()
