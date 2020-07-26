from django.contrib import admin
from .models import Course, Quiz, Choice, Quizgame, AttemptedQuestion
# Register your models here.

admin.site.register(Course)
admin.site.register(AttemptedQuestion)

class ChoiceInline(admin.StackedInline):
    model = Choice
    max_num = 4
    min_num = 1

@admin.register(Quiz)
class Quiz(admin.ModelAdmin):
    list_display = ('question','course_name')
    inlines = (ChoiceInline,)


@admin.register(Quizgame)
class Quizgame(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'start_time', 'finish_time')


