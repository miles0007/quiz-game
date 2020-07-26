import random, math, datetime
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name}"


class Quiz(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course')
    question = models.TextField(max_length=100)
    maximum_marks = models.DecimalField(
        'Maximun_Marks', default=1, decimal_places=2, max_digits=6)
    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="choice_question")
    choice = models.CharField(max_length=100)
    is_true = models.BooleanField("This is Correct Answer", default=False)

    def __str__(self):
        return self.choice

class Quizgame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.DecimalField("Total score", default=0, decimal_places=2, max_digits=6)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)
    def __str__(self):
        return f"Quizgame user:{self.user}"
    
    def get_new_question(self):
        used_question = AttemptedQuestion.objects.filter(quiz_profile=self).values_list('question__id',flat=True)
        remaining_questions = Quiz.objects.filter(course_name__id=self.course.id).exclude(id__in=used_question)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)
    
    def create_attempt(self, question):
        attempted_question = AttemptedQuestion(question=question, quiz_profile=self)
        attempted_question.save()

    def end_time(self,time,quiz_id):
        time_obj = Quizgame.objects.get(id=quiz_id)
        time_obj.finish_time = time
        time_obj.save()

    def update_score(self):
        score_objects = Quizgame.objects.get(id=self.id)
        score_objects.total_score += 1
        score_objects.save()


class AttemptedQuestion(models.Model):
    quiz_profile = models.ForeignKey(Quizgame, on_delete=models.CASCADE, related_name='attempt')
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_true = models.BooleanField(default=False)
    mark_obtained = models.DecimalField(
        "Marks Obtained", default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return f"{self.quiz_profile} = {self.question.id}" 
