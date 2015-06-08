from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    image = models.ImageField(upload_to='users', default='users/default_user.png')

    def __str__(self):
        return "%s profile" % self.user.username


class UserPages(models.Model):
    user = models.ForeignKey(User)
    page_id = models.CharField(max_length=50, null=False, blank=False)
    page_name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='accounts', default='accounts/default_account.png')

    def __str__(self):
        return "%s pages" % self.user.username


class UserPagePosts(models.Model):
    page = models.ForeignKey(UserPages)
    post_id = models.CharField(max_length=100, null=False, blank=False)
    post_url = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return "%s: %s" % (self.post_id, self.post_url)