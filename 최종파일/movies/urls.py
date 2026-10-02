from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.movie_list_api, name='movie_list_api'),  
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    #path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
]
