from django.contrib.auth.models import AbstractUser
from django.db import models

# from lms.constants import USER_MODEL
# from lms.models import Course, Lesson


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
    # city = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     null=True,
    #     verbose_name="Город",
    #     help_text="Укажите ваш город",
    # )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


# class Payment(models.Model):
#     CASH = "Наличные"
#     TRANSFER = "pm_card_visa"
#
#     STATUS_CHOICES = [
#         (CASH, "Наличные"),
#         (TRANSFER, "Перевод на счет"),
#     ]
#
#     user = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         verbose_name="Пользователь",
#         related_name="payments",
#     )
#     payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
#     paid_course = models.ForeignKey(
#         Course,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name="Оплаченный курс",
#     )
#     paid_lesson = models.ForeignKey(
#         Lesson,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name="Оплаченный урок",
#     )
#     amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
#     payment_method = models.CharField(
#         max_length=30,
#         choices=STATUS_CHOICES,
#         default=TRANSFER,
#         verbose_name="метод оплаты",
#     )
#     session_id = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
#         verbose_name="ID сессии",
#         help_text="Укажите ID сессии для перевода на счет",
#     )
#     link = models.URLField(
#         max_length=400,
#         null=True,
#         blank=True,
#         verbose_name="Ссылка на оплату",
#         help_text="Укажите ссылку на оплату",
#     )
#
#     class Meta:
#         verbose_name = "Платеж"
#         verbose_name_plural = "Платежи"
#
#     def __str__(self):
#         return f"{self.user} - {self.payment_date}"
