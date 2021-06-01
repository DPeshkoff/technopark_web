"""technopark_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static


from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('new/', views.new_questions, name='new_questions'),
    path('popular/', views.popular_questions, name='popular_questions'),

    path('question/<int:pk>/', views.question, name='question'),
    path('tag/<str:tag>', views.tags, name='tags'),

    path('new-question/', views.new_question, name='new_question'),

    path('settings/', views.settings, name='settings'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('', views.new_questions, name='root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
