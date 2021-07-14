from django.db import models
# from django.db.models import Avg
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True
    )
    bio = models.TextField(null=True, blank=True, verbose_name="О себе")
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='User')

# class Review(models.Model):

#     text = models.CharField(
#         verbose_name='Рецензия',
#         help_text='Введите текст рецензии')

#     tilte = models.ForeignKey(
#         Title, on_delete=models.CASCADE, related_name="review")

#     pub_date = models.DateTimeField(
#         "Дата добавления", auto_now_add=True, db_index=True)

#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="review")

#     score = models.IntegerField(
# validators=[MinValueValidator(1), MaxValueValidator(10)],
# help_text="оцените от 1 до 10")

#     def __str__(self):
#         return self.text[:15]

#     class Meta:
#         verbose_name = 'Рецензия'
#         verbose_name_plural = 'Рецензии'

#     # def overall_rating(self):
#     #     return self.objects.aggregate(Avg('score'))


# class Comment(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="comments"
#     )
#     review = models.ForeignKey(
#         Review, on_delete=models.CASCADE, related_name="comments"
#     )
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         "Дата добавления", auto_now_add=True, db_index=True
#     )

#     def __str__(self):
#         return self.text[:15]

#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'
#         ordering = ('-pub_date',)
