from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Post(models.Model):  # 이 부분 실제 DB로 연결할 필요가 있습니다. 글 번호 등, 필요한 요소 더 넣을 수 있습니다.
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ Comment 모델 추가
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 댓글이 달린 게시글
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()  # 댓글 본문
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies') # ✅ 대댓글용 자기참조 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)      # 수정일
    
    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'


    