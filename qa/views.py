from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from qa.models import Question, Answer


def test(_):
    return HttpResponse('OK')


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


@require_GET
def question_details(request, num):
    question = get_object_or_404(Question, id=num)
    try:
        answers = Answer.objects.filter(question=question)
    except Answer.DoesNotExist:
        answers = None
    return render(request, 'question_detail.html', {
        'title':   question.title,
        'text':    question.text,
        'answers': answers.all()[:]
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
