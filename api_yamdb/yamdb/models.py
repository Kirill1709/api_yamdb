from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title.rating = Review.objects.filter(
            title=self.id).aggregate(Avg('score'))['score__avg']
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
