from django import forms
from django.contrib.auth.models import User
from .models import Question, Answer


MAX_USERNAME_LENGTH = 50
MAX_EMAIL_LENGTH    = 100
MAX_PASSWORD_LENGTH = 20


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=250, label='Теги',
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Введите теги через пробел"}),
                           error_messages={'required': 'Введите хотя бы один тег'})

    class Meta:
        model = Question
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст вопроса'}),
        }
        error_messages = {'title': {'required': 'Введите заголовок'},
                          'description': {'required': 'Введите текст вопроса'}}

    def clean(self):
        cleaned_data = super(AskForm, self).clean()

        if len(cleaned_data['tags'].split()) > 10:
            raise forms.ValidationError("Нельзя добавить больше 10 тегов")

        return cleaned_data

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control mb-3',
                                                    'placeholder': 'Введите текст ответа'})}
        error_messages = {'content': {'required': 'Введите текст ответа'}}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}),
                               error_messages={'required': 'Введите пароль'})


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    email = forms.EmailField(max_length=MAX_EMAIL_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
                               error_messages={'required': 'Введите e-mail'})

    nickname = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ник на сайте'}),
                               error_messages={'required': 'Введите ник'})


    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                               error_messages={'required': 'Введите пароль'})

    confirm_password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Подтвердите пароль'}),
                                       error_messages={'required': 'Введите подтверждение пароля'})

    
    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'user-avatar'}))

    def clean_username(self):
        cleaned_data = super(RegisterForm, self).clean()
        if User.objects.filter(username=cleaned_data['username']).exists():
            raise forms.ValidationError('Такой логин уже существует')

        return cleaned_data['username']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

class EditForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    nickname = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ник на сайте'}),
                               error_messages={'required': 'Введите ник'})

    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'user-avatar'}))

    email = forms.EmailField(max_length=MAX_EMAIL_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
                               error_messages={'required': 'Введите e-mail'})


