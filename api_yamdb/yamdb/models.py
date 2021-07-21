import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True, verbose_name='О себе')
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=USER)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Genre(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        db_index=True,
        validators=(MaxValueValidator(datetime.datetime.now().year),)
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(Category, blank=True,
                                 on_delete=models.SET_NULL,

                                 related_name='titles', null=True)

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):

    text = models.TextField(
        verbose_name='Рецензия',
        help_text='Введите текст рецензии')

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="review")

    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review")

    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)
                    ], help_text="оцените от 1 до 10")

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        unique_together = ('title', 'author', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title.rating = Review.objects.filter(
            title_id=self.title).aggregate(Avg('score'))['score__avg']
        self.title.save()


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
