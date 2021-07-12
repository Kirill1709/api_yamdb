from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    RATING = ((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),)

    text = models.CharField(
        verbose_name='Рецензия',
        help_text='Введите текст рецензии')

    tilte = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="review")

    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review"
    )

    score = models.IntegerField(choices=RATING, help_text="оцените от 1 до 10")

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def overall_rating(self):
        return self.objects.aggregate(sum('score'))


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
