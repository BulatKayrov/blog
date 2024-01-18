from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from .utils import verified_accounts


class User(AbstractUser):
    image = models.ImageField(upload_to='users/', blank=True)
    code_verified = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'



