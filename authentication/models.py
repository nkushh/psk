from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models

from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	psk_region = models.CharField(max_length=200, blank=True)
	usertype = models.CharField(max_length=200, blank=True)
	phone_no = models.CharField(max_length=15, blank=True)
	last_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

