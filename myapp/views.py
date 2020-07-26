import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm
from .models import Quiz, Quizgame, Choice, AttemptedQuestion, Course
# Create your views here.



def index(request):
    '''
    Base Layout
    '''
    return render(request,'layout.html')

def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password2'))
            new_user.save()
            return redirect('Quiz:login')
        
        else:   # for sending the error meassage to the form
            return render(request, 'account/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request,'account/register.html',{'form':form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # print(username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Quiz:profile')
            else:
              messages.warning(request, "Invalid Username and Password")

    form = LoginForm()
    return render(request,"account/login.html",{"form":form})


def user_logout(request):
    logout(request)
    return redirect('Quiz:login')


@login_required
def profile(request):
    courses = Course.objects.all()
    context = {"courses":courses}
    return render(request, 'quiz/courses.html',context=context)

@login_required
def quiz_start(request,course_id):
    # "course name" passed via instance, Getting the instance name from id
    course_name = Course.objects.filter(id=course_id)
    try:
        check_user = Quizgame.objects.get(user=request.user, course=course_name[0])
        if check_user is not None:
            return render(request, "quiz/error_page.html")
    except: pass
    # initialize the quiz_profile for the user with quiz_id
    quiz_profile, created = Quizgame.objects.get_or_create(
        user=request.user, course=course_name[0])
    return render(request, 'account/profile.html')
    

@login_required
def quiz_progress(request):
    #  get the user profile count to check more the one profile for the user
    quiz_profile_count = Quizgame.objects.filter(user=request.user).count()
    
    # if one profile means "using get() method"
    if quiz_profile_count == 1:
        quiz_id = Quizgame.objects.filter(user=request.user).first()
        quiz_profile = Quizgame.objects.get(id=quiz_id.id,user=request.user)
    
    # else filter out the last object
    else:
        quiz_id = Quizgame.objects.filter(user=request.user).last()
        quiz_profile, created = Quizgame.objects.get_or_create(id=quiz_id.id,user=request.user)
    
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        value = request.POST.get("choices")
        
        # getting answer object by question_id
        answer = Choice.objects.get(question_id=question_id, is_true=True)
        result = getattr(answer, 'choice')
        # update the finish time
        quiz_profile.end_time(datetime.datetime.now(),quiz_id.id)

        if str(value) != str(answer):
            message = False
            context = {"message": message,
                       "answer": result}
            return render(request, "quiz/answer_validator.html", context=context)

        else:
            # increment the score by +1
            quiz_profile.update_score()
            message = True
            context = {"message": message}
            return render(request, "quiz/answer_validator.html", context=context)

    # get new question for the quiz_profile
    question = quiz_profile.get_new_question()

    # check if remaining questions exists
    if question is not None:
        quiz_profile.create_attempt(question)

    # if no remaining questions exists
    if question is None:
        return redirect('Quiz:end')
    context = {'question': question}
    return render(request, 'quiz/display_question.html', context=context)


@login_required
def final_part(request):
    #  get the user profile count to check more the one profile for the user
    quiz_profile_count = Quizgame.objects.filter(user=request.user).count()
    
    # if one profile means "using get() method"
    if quiz_profile_count == 1:
        obj = Quizgame.objects.get(user=request.user)
    
    # else filter out the last object
    else:
        quiz_id = Quizgame.objects.filter(user=request.user).last()
        obj, created = Quizgame.objects.get_or_create(
            id=quiz_id.id, user=request.user)
    
    # calculating the time taken for the quiz object
    start = obj.start_time
    end = obj.finish_time
    score = getattr(obj, 'total_score')
    try:
        result = end - start
        result = round(result.total_seconds())
    except TypeError:
        return HttpResponse("Not attended the test Properly")
    context = {"result": result, "score":score}
    return render(request, "quiz/result_page.html",context=context)


@login_required
def leaderboard(request):
    objects = Quizgame.objects.filter(user=request.user)
    context = {"objects":objects}
    return render(request,"quiz/leaderboard.html",context=context)
