# Generated by Django 2.2.6 on 2021-07-20 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0003_auto_20210720_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
