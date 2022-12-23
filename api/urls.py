from django.urls import path, include
from home.views import *
from blog.views import (PostApiView,)

urlpatterns = [
    path('animals/', AnimalView.as_view()),
    path('blogs/', PostApiView.as_view()),
    path('animal-create/', AnimalCreateApi.as_view()),
    path('register/', RegisterApi.as_view()),
    path('login/', LoginApi.as_view()),
    path('animal/<pk>/', AnimalDetailView.as_view()),
]
