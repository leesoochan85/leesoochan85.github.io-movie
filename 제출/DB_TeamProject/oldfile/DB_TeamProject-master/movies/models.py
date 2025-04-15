from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(null=True) #리뷰와 연동하기 위해
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField(default=0)
    genres = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

#영화와 리뷰를 연동하기 위해 모델 생성
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"{self.movie.title} - {self.author}"
        
# Create your models here.
