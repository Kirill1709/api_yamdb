from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Genre(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(Category, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles', null=True)
    rating = models.IntegerField(blank=True, null=True)


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
