# Generated by Django 3.0.8 on 2020-07-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200724_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizgame',
            name='finish_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quizgame',
            name='start_time',
            field=models.IntegerField(default=1595597208.0199904),
        ),
    ]