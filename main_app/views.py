from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

questions = [
    {'id': i + 1,
     'title': f'Заголовок вопроса №{i + 1}',
     'description': 'Описание вопроса',
     'num_of_answers': 5,
     'num_of_likes': 99,
     'author': 'Карпухин',
     'tags': ['arduino', 'amplifiers']}
    for i in range(100)
]


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
    page = paginate(questions, request, 10)
    return render(request, 'new_questions.html', {
        'page_obj': page
    })


def popular_questions(request):
    page = paginate(questions, request, 10)
    return render(request, 'popular_questions.html', {
        'page_obj': page
    })


def question(request, pk):
    question = questions[pk - 1]
    answers = [{'id': i + 1,
                'author': f'студент_иу6',
                'text': f'Ответ №{i + 1}\n Примерный текст ответа. ',
                'rating': 4}
               for i in range(32)]
    page = paginate(answers, request, 10)
    return render(request, 'question.html', {
        'question': question,
        'page_obj': page
    })


def tags(request, tag):
    page = paginate(questions, request, 10)
    return render(request, 'tag.html', {
        'page_obj': page,
        'tag': tag
    })


