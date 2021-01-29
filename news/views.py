from django.contrib import messages
from django.contrib.auth import get_user, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import FormsNews, UserRegisterForm, LoginRegisterForm
from django.http import HttpResponse

from .models import News, Category
from django.contrib.auth.forms import UserCreationForm


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)
class HomeNews(ListView):
    template_name = "news/index.html"
    model = News
    context_object_name = "news"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новости"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)
#
#


class NewsByCategory(ListView):
    model = News
    template_name = "news/category.html"
    context_object_name = "news"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs["category_id"], is_published=True)


# Возвращает страницу, с категориями(определенные)
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     return render(request, 'news/category.html', {'news': news})


class ViewNews(DetailView):
    """
    Автоматически выполняет код ниже
      news_item = get_object_or_404(News, pk=news_id)
     return render(request, 'news/view_news.html', {'news_item': news_item})
     """
    model = News
    template_name = "news/view_news.html"
    context_object_name = "news_item"


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


def add_news(request):
    if request.method == "POST":
        form = FormsNews(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect(news)
    else:
        form = FormsNews()
    return render(request, "news/add_news.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form)
            messages.success(request, "Вы зарегистрировались")
        else:
            messages.error(request, "Ошибка")
    else:
        form = UserRegisterForm()
    return render(request, "news/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginRegisterForm()
    return render(request, "news/login.html", {"form": form})
def user_logout(request):
    logout(request)
    return redirect("home")
