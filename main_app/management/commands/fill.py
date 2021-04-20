from django.core.management.base import BaseCommand, CommandError
from main_app.models import *
from random import choice, sample, randint
from faker import Faker

fake = Faker(["en_US"])

# python3 manage.py fill --users 100 --questions 10000 --answers 100000 --tags 100 --votes 200000

class Command(BaseCommand):
    help = 'Fill DB'

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, help="Количество профилей")
        parser.add_argument("--questions", type=int, help="Количество вопросов")
        parser.add_argument("--answers", type=int, help="Количество ответов к вопросу")
        parser.add_argument("--tags", type=int, help="Количество тегов")
        parser.add_argument("--votes", type=int, help="Количество оценок к вопросу")

    def handle(self, *args, **kwargs):
        try:
            profiles_count = kwargs["users"]
            questions_count = kwargs["questions"]
            answers_per_question_count = kwargs["answers"]
            tags_count = kwargs["tags"]
            votes_per_question_number = kwargs["votes"]
        except:
            raise CommandError("Some arguments were not provided")

        self.generate_profiles(profiles_count)
        self.generate_tags(tags_count)
        self.generate_questions(questions_count)
        self.generate_answers(answers_per_question_count)

    def generate_users(self, count):
        for i in range(0, count):
            User.objects.create_user(fake.unique.last_name(), fake.first_name(),
                                     fake.unique.password(length=fake.random_int(min=8, max=16)))

    def generate_profiles(self, count):
        self.generate_users(count)

        users_ids = list(User.objects.values_list("id", flat=True))
        for i in range(0, count):

            UserProfile.objects.create(user_id=users_ids[i], username=fake.unique.last_name())

    def generate_tags(self, count):
        for i in range(count):
            Tag.objects.create(tag_name=fake.unique.word())

    def generate_questions(self, count):
        profiles = list(UserProfile.objects.values_list("id", flat=True))

        for i in range(count):
            question = Question.objects.create(
                author_id=choice(profiles),
                title=fake.sentence(nb_words=3),
                description=fake.text()
            )

            tags_count = Tag.objects.count()

            tags = list(set([Tag.objects.get(id=randint(1, tags_count)) for j in range(randint(1, tags_count))]))

            question.tags.set(tags)



    def generate_answers(self, count):
        profiles = list(UserProfile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        for question_id in questions:
            for i in range(count):
                answer = Answer.objects.create(
                    author_id=choice(profiles),
                    related_question_id=question_id,
                    content=fake.text()
                )