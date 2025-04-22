from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Не задано поле электронной почты")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Укажите свой email"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    tg_nick = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="ТГ-ник",
        help_text="Укажите телеграмм-ник"
    )
    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Телеграмм chat-id",
        help_text="Укажите телеграмм chat-id"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
