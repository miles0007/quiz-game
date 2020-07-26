# Generated by Django 3.0.8 on 2020-07-24 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quizgame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Total score')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=100)),
                ('maximum_marks', models.DecimalField(decimal_places=2, default=1, max_digits=6, verbose_name='Maximun_Marks')),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_course', to='myapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('is_true', models.BooleanField(default=False, verbose_name='This is Correct Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice_question', to='myapp.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='AttemptedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_true', models.BooleanField(default=False)),
                ('mark_obtained', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Marks Obtained')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Quiz')),
                ('quiz_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempt', to='myapp.Quizgame')),
            ],
        ),
    ]
