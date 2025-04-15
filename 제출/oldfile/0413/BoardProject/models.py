from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):  # 이 부분 실제 DB로 연결할 필요가 있습니다. 글 번호 등, 필요한 요소 더 넣을 수 있습니다.
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ Comment 모델 추가
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 댓글이 달린 게시글
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()  # 댓글 본문
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)      # 수정일

    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'
    
class Movies(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    vote_average = models.FloatField()
    genres = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Movies"

class Review(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='reviews', null=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    translated_content = models.TextField(blank=True, null=True)  # 이미 null=True로 설정됨
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.author} for {self.movie.title}"

class ReviewComment(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='review_comments', null=True) #null = True는 실제 데이터 채우면 지워도 됩니다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # null=True 추가
    updated_at = models.DateTimeField(auto_now=True, null=True)  # null=True 추가
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.movie.title}"
