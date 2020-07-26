from django.urls import path
from . import views

app_name = 'Quiz'

urlpatterns = [
    path('',views.index, name='home'),
    path('register/',views.user_register, name='register'),
    path('login/',views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('quiz/<int:course_id>',views.quiz_start, name='quiz_'),
    path('quiz_progress/',views.quiz_progress, name='quiz_progress'),
    path('end_section/',views.final_part, name='end'),
    path('leaderboard/',views.leaderboard, name='score_board')

]
