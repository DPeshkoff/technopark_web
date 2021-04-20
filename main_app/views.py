from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main_app.models import UserProfile, Question, Answer
from django.core.exceptions import ObjectDoesNotExist

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return page


def new_question(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')
#

def new_questions(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, 10)
    return render(request, 'new_questions.html', {
        'page_obj': page
    })


def popular_questions(request):
    questions = Question.objects.popular_questions()
    page = paginate(questions, request, 10)
    return render(request, 'popular_questions.html', {
        'page_obj': page
    })


def question(request, pk):
    try:
        question = Question.objects.get(id=pk)
        answers = question.answers.best_answers()
        page = paginate(answers, request, 10)
        return render(request, 'question.html', {
            'question': question,
            'page_obj': page
        })
    except ObjectDoesNotExist:
        return render(request, '404.html')



def tags(request, tag):
    questions = Question.objects.questions_for_tag(tag).all()
    page = paginate(questions, request, 10)
    return render(request, 'tag.html', {
        'page_obj': page,
        'tag': tag
    })


