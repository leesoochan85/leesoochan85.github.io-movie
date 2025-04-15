import os
import django

# settings.py 경로 정확하게 지정!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_TeamProject.settings")
django.setup()

from BoardProject.models import Movies

# 테스트용 더미 데이터 생성
movie = Movies.objects.create(
    title="테스트 영화",
    overview="이것은 테스트용 영화입니다.",
    release_date="2024-01-01",
    vote_average=9.1,
    genres="드라마"
)

print("🎬 더미 영화 생성 완료:", movie)
