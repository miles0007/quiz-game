# Generated by Django 3.0.8 on 2020-07-24 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20200724_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizgame',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
