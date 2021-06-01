from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main_app.models import UserProfile, Question, Answer, Tag
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import *

def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return page


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')


def new_questions(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, 20)
    return render(request, 'new_questions.html', {
        'page_obj': page
    })


def popular_questions(request):
    questions = Question.objects.popular_questions()
    page = paginate(questions, request, 20)
    return render(request, 'popular_questions.html', {
        'page_obj': page
    })


def question(request, pk):
    try:
        question = Question.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, '404_not_found.html')

    answers = question.answers.best_answers()
    page = paginate(answers, request, 20)
    if not request.user.is_authenticated:
        return render(request, 'question.html', {
            'question': question,
            'page_obj': page
        })

    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.userprofile
            answer.related_question = question
            answer.save()

            response = redirect(reverse('question', kwargs={'pk': question.id}))
            response['Location'] += f'#ans{answer.id}'
            return response

    return render(request, 'question.html', {
        'question': question,
        'page_obj': page,
        'form': form
    })



def tags(request, tag):
    questions = Question.objects.questions_for_tag(tag).all()
    page = paginate(questions, request, 20)
    return render(request, 'tag.html', {
        'page_obj': page,
        'tag': tag
    })


@login_required
def new_question(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.userprofile
            question.save()

            tags = list(set(form.cleaned_data['tags'].split()))
            with transaction.atomic():
                tags_objects = [Tag.objects.get_or_create(tag_name=tag)[0] for tag in tags]
            question.tags.set(tags_objects)

            return redirect(reverse('question', kwargs={'pk': question.id}))

    return render(request, 'ask.html', {'form': form})


def login(request):
    if request.method == 'GET':
        request.session['next_page'] = request.GET.get('next', '/')
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.session.pop('next_page', '/'))

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'GET':
        request.session['next_page'] = request.GET.get('next', '/')
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'])

            userprofile = UserProfile.objects.create(user=user, email=form.cleaned_data['email'], nickname=form.cleaned_data['nickname'])
            if form.cleaned_data['profile_pic'] is not None:
                userprofile.profile_pic = form.cleaned_data['profile_pic']
                userprofile.save()

            auth.login(request, user)
            return redirect(request.session.pop('next_page', '/'))

    return render(request, 'register.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'GET':
        form = EditForm(initial={"username": request.user.username,
                                 "nickname": request.user.userprofile.nickname})
    else:
        form = EditForm(request.POST, request.FILES, initial={"username": request.user.username,
                                                              "nickname": request.user.userprofile.nickname})
        if form.is_valid():
            user = request.user
            userprofile = user.userprofile
            if 'username' in form.changed_data:
                user.username = form.cleaned_data['username']
            if 'email' in form.changed_data:
                userprofile.email = form.cleaned_data['email']
            if 'nickname' in form.changed_data:
                userprofile.nickname = form.cleaned_data['nickname']
            if 'profile_pic' in form.changed_data:
                userprofile.profile_pic = form.cleaned_data['profile_pic']
            userprofile.save()
            user.save()

    return render(request, 'settings.html', {'form': form})
