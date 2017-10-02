from django.contrib.auth import authenticate
from django.contrib.auth import login as authlogin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET

from qa.forms import AnswerForm, AskForm, LoginForm, RegisterForm
from qa.models import Question, Answer


@require_GET
def index(request):
    questions_list = Question.objects.new()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(questions_list, limit)
    paginator.baseurl = 'question/'
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'questions': questions})


def question_details(request, num):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        form._user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.get_full_path())
        else:
            return HttpResponse('OK')
    else:
        question = get_object_or_404(Question, id=num)
        try:
            answers = Answer.objects.filter(question=question)
        except Answer.DoesNotExist:
            answers = None
        return render(request, 'question_detail.html', {
            'title':   question.title,
            'text':    question.text,
            'answers': answers.all()[:],
            'form':    AnswerForm(initial={'question': num}),
            'path':    request.get_full_path(),
            'user':    request.user
        })


@require_GET
def popular(request):
    questions_list = Question.objects.popular()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(questions_list, limit)
    paginator.baseurl = '../question/'
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'popular.html', {'questions': questions})


def add_question(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect('/question/{}/'.format(obj.id))
        else:
            return HttpResponse('OK')
    else:
        return render(request, 'new_question.html', {
            'title': 'New question',
            'form':  AskForm(),
            'path':  '/ask/',
            'user':  request.user
        })


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                authlogin(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'login.html', {
            'title': 'Login',
            'form': form,
            'path':  '/login/',
        })
    else:
        return render(request, 'login.html', {
            'title': 'Login',
            'form':  LoginForm(),
            'path':  '/login/',
        })


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                authlogin(request, user)
                return HttpResponseRedirect('/')
        return HttpResponse('OK')
    else:
        return render(request, 'register.html', {
            'title': 'Signup',
            'form':  RegisterForm(),
            'path':  '/signup/',
        })
