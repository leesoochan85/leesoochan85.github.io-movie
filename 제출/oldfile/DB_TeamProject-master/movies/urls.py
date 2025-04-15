from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('api/', views.MovieListAPIView.as_view(), name='movie_list_api'),
]
