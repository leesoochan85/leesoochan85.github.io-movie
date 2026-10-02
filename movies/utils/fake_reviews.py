# movies/utils/fake_reviews.py

import os
import sys
import django
import random
from faker import Faker

# Django 환경 세팅
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_TeamProject.settings")
django.setup()

from movies.models import Movie, Review

faker = Faker("ko_KR")

korean_sentences = [
    "정말 감동적인 영화였어요.", "배우들의 연기가 뛰어났습니다.",
    "스토리 전개가 흥미로웠어요.", "다시 보고 싶은 작품이에요.",
    "음악과 영상미가 인상 깊었어요.", "예상치 못한 반전이 있었어요.",
    "가족과 함께 보기 좋은 영화입니다.", "긴장감 넘치는 전개가 좋았어요.",
    "웃기고 재미있는 영화였습니다.", "눈물이 나는 장면이 많았어요.",
    "조금 지루한 부분도 있었지만 괜찮았어요.", "다음 시리즈가 기대됩니다.",
    "현실적인 내용이라 공감이 됐어요.", "캐릭터들이 매력 있었어요.",
    "완성도 높은 영화였어요."
]

def create_fake_reviews_per_movie(n=3):
    movies = Movie.objects.all()
    total_reviews = 0

    for movie in movies:
        for _ in range(n):
            author = faker.name()
            content = " ".join(random.sample(korean_sentences, 2))
            Review.objects.create(movie=movie, author=author, content=content)
            total_reviews += 1

    print(f"✅ 총 {total_reviews}개의 페이크 리뷰가 생성되었습니다.")

if __name__ == "__main__":
    create_fake_reviews_per_movie(n=3)
