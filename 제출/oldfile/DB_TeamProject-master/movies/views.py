from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from django.views import View

def movie_list(request):
    movies = Movie.objects.all()
    total_count = movies.count()  # 전체 영화 수 계산
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'total_count': total_count,  # 템플릿에서 사용할 변수
    })

class MovieListAPIView(View):
    def get(self, request, *args, **kwargs):
        movies = Movie.objects.all().values('id', 'title', 'overview', 'release_date', 'vote_average', 'genres')
        return JsonResponse({'movies': list(movies)}, safe=False)