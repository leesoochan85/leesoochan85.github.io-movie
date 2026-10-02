from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import  Movie, Review
from django.db.models import Q  # 검색용
import random
from django.http import JsonResponse

def movie_list(request):
    query = request.GET.get('q', '')  # 검색어 받기

    if query:
        movies = Movie.objects.filter(Q(title__icontains=query))
    else:
        movies = Movie.objects.all()

    total_count = movies.count() # 전체 영화 수 계산

   # 🎯 평점 높은 영화 중 랜덤으로 4개 추천
    high_rated_movies = Movie.objects.filter(vote_average__gte=8.0)  # 평점 8.0 이상
    top_movies = random.sample(list(high_rated_movies), min(len(high_rated_movies), 4))

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'total_count': total_count,
        'top_movies': top_movies,  # 👉 템플릿에서 사용할 변수
        'query': query  # 검색창에 입력 유지
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()  # related_name='reviews' 덕분에 이렇게 호출 가능
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews})   

def movie_list_api(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query))
    else:
        movies = Movie.objects.all()

    movie_data = [{
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'release_date': movie.release_date,
        'vote_average': movie.vote_average,
        'genres': movie.genres,
    } for movie in movies]

    return JsonResponse({'movies': movie_data})