from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeNews.as_view(), name="home"),
    path("register/", register, name="register"),
    path('login/', user_login, name="login"),
    path('category/<int:category_id>/',
         NewsByCategory.as_view(), name="category"),
    path('news/<int:pk>/', ViewNews.as_view(), name="news"),
    path('news/add_news/', add_news, name="add_news"),
    path("logout/", user_logout, name="logout"),
]
