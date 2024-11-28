from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def create_path_to_upload_images(instance: 'Profile', name: str) -> str:
    return f'users_files/user_{instance.user.pk}/photos/img_{name}'


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True ,validators=[MinValueValidator(1), MaxValueValidator(120)])
    avatar = models.ImageField(null=False, blank=True, upload_to=create_path_to_upload_images)

    def __str__(self):
        return f'{self.user.first_name or self.user.username}'
