# Generated by Django 3.0.8 on 2020-07-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200724_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizgame',
            name='end_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='quizgame',
            name='start_time',
            field=models.IntegerField(default=1595592931.853158),
        ),
    ]
