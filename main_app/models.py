from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username = models.CharField(max_length=60, verbose_name='Имя пользователя')

    # TODO - profile pictures

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class QuestionManager(models.Manager):

    def new_questions(self):
        return self.order_by()

    def popular_questions(self):
        return self.order_by("-rating")

    def questions_for_tag(self, tag):
        return self.filter(tags__tag_name=tag)


class Question(models.Model):

    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    title = models.CharField(max_length=80, verbose_name='Заголовок вопроса')

    description = models.TextField(verbose_name='Описание вопроса')

    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')

    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='questions', related_query_name='question')

    objects = QuestionManager()

    def get_answers_count(self):
        return self.answers.count()

    def update_rating(self):
        self.rating = QuestionVote.objects.get_rating(self.id)
        self.save()

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['rating'])
        ]

        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):

    def best_answers(self):
        return self.order_by("-rating")


class Answer(models.Model):

    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    related_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers", related_query_name="answer")

    text = models.TextField(verbose_name='Текст ответа')

    rating = models.IntegerField(default=0, verbose_name='Рейтинг ответа')

    is_marked = models.BooleanField(default=False, verbose_name='Отметка на ответе')

    objects = AnswerManager()


    def update_rating(self):
        self.rating = AnswerVote.objects.get_rating(self.id)
        self.save()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.content


class VoteManager(models.Manager):
    
    LIKE = 1

    DISLIKE = -1

    def get_likes(self, pk):
        return self.filter(id=pk, mark=VoteManager.LIKE).count()

    def get_dislikes(self, pk):
        return self.filter(id=pk, mark=VoteManager.DISLIKE).count()

    def get_rating(self, pk):
        return self.get_likes(pk) - self.get_dislikes(pk)


class QuestionVote(models.Model):

    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name='Автор оценки')

    mark = models.IntegerField(default=0, verbose_name='Поставленная оценка')

    related_question = models.ForeignKey('Question', verbose_name='Оцениваемый вопрос', on_delete=models.CASCADE)

    objects = VoteManager()

    class Meta:
        verbose_name = 'Оценка вопроса'
        verbose_name_plural = 'Оценки вопросов'

    def __str__(self):
        return f'Оценка вопроса: {self.mark}'


class AnswerVote(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name='Автор оценки')

    mark = models.IntegerField(default=0, verbose_name='Поставленная оценка')  

    objects = VoteManager()

    related_answer = models.ForeignKey('Answer', verbose_name='Оцениваемый ответ', on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка ответа: {self.mark}'

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответов'


class Tag(models.Model):

    tag_name = models.CharField(max_length=50, unique=True, verbose_name='Название тега')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'