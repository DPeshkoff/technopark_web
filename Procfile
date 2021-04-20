web: python3 manage.py sqlflush
web: python3 manage.py makemigrations
web: python3 manage.py migrate
web: python3 manage.py fill --users 100 --questions 10000 --answers 100000 --tags 100 --votes 200000
web: gunicorn technopark_web.wsgi --log-file -