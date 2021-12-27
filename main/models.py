from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'


class Workout(models.Model):
    title = models.CharField( max_length=255)
    time = models.DateTimeField(verbose_name='время тренировки')

    def __str__(self):
        return f'{self.title}'
