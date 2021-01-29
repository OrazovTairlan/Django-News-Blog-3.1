from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import News, Category
import re
from django.contrib.auth.models import User


class LoginRegisterForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class FormsNews(forms.ModelForm):
    class Meta:
        model = News # отсюда из модели, в файле forms: news = form.save()
                         # сохраняется объект в модель, которая указана в model.
                         # Если мы установим model = Category, то сохраняться объект будет в модели Category
        fields = ["title"]
        # widgets = {
        #     'content': forms.Textarea(attrs={'rows': 1, "style": "height:25px"}),
        # }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r'^ \d', title):
            raise ValidationError("Название не должно начинаться с цифры")
        return title
