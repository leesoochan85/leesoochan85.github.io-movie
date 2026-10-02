# # movies/utils/fetch_movies.py

# import requests
# import random
# import time
# from faker import Faker
# from django.conf import settings  # settings.py에 TMDB_API_KEY를 설정해두었다고 가정
# from movies.models import Movie

# faker = Faker('ko_KR')

# # 영화 리뷰나 코멘트 생성을 위한 예제 문장
# korean_sentences = [
#     "정말 감동적인 영화였어요.", "배우들의 연기가 뛰어났습니다.",
#     "스토리 전개가 흥미로웠어요.", "다시 보고 싶은 작품이에요.",
#     "음악과 영상미가 인상 깊었어요.", "예상치 못한 반전이 있었어요.",
#     "가족과 함께 보기 좋은 영화입니다.", "긴장감 넘치는 전개가 좋았어요.",
#     "웃기고 재미있는 영화였습니다.", "눈물이 나는 장면이 많았어요.",
#     "조금 지루한 부분도 있었지만 괜찮았어요.", "다음 시리즈가 기대됩니다.",
#     "현실적인 내용이라 공감이 됐어요.", "캐릭터들이 매력 있었어요.",
#     "완성도 높은 영화였어요."
# ]

# # TMDB API 키 설정 (settings.py에 TMDB_API_KEY가 설정되어 있거나 직접 입력)
# TMDB_API_KEY = getattr(settings, 'TMDB_API_KEY', '133e8ffdf21c352386b08f91ca7054f0')

# # 장르 매핑 사전
# GENRE_MAP_KR = {
#     28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디", 80: "범죄", 99: "다큐멘터리",
#     18: "드라마", 10751: "가족", 14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
#     9648: "미스터리", 10749: "로맨스", 878: "SF", 10770: "TV 영화", 53: "스릴러",
#     10752: "전쟁", 37: "서부"
# }

# def fetch_movies(page):
#     """
#     TMDB API를 사용해 인기 영화 데이터(한글)를 가져옵니다.
#     """
#     url = (
#         f"https://api.themoviedb.org/3/movie/popular?"
#         f"api_key={TMDB_API_KEY}&language=ko-KR&sort_by=release_date.desc&page={page}"
#     )
#     response = requests.get(url)
#     return response.json().get("results", [])

# def save_movies(limit=200):
#     """
#     TMDB API로부터 영화 데이터를 받아와, limit 수만큼 Movie 객체를 생성합니다.
#     """
#     saved = 0
#     # 1~10 페이지까지 반복 (필요에 따라 페이지 범위를 조정)
#     for page in range(1, 11):
#         if saved >= limit:
#             break
#         movies_list = fetch_movies(page)
#         for movie in movies_list:
#             if saved >= limit:
#                 break
#             title = movie.get('title') or movie.get('original_title')
#             if not title:
#                 continue
#             overview = movie.get('overview') or "줄거리 정보 없음"
#             release_date = movie.get('release_date') or None
#             vote_average = round(movie.get('vote_average', 0), 1)
#             genre_ids = movie.get('genre_ids', [])
#             genre_names = [GENRE_MAP_KR.get(gid, f"ID:{gid}") for gid in genre_ids]
#             genres_str = ", ".join(genre_names)

#             # Django ORM을 사용하여 Movie 객체 생성
#             Movie.objects.create(
#                 title=title,
#                 overview=overview,
#                 release_date=release_date,
#                 vote_average=vote_average,
#                 genres=genres_str
#             )
#             saved += 1
#         print(f"🎬 저장된 영화 수: {saved}")
#         time.sleep(0.1)
#     return saved

# # ---
# # 아래는 필요에 따라 추가 데이터(유저, 게시글, 댓글 등)를 생성하는 예시입니다.
# # 여러분 프로젝트에 맞는 모델(예: User, Post, Comment, Review, ReviewComment 등)이 있어야 작동합니다.
# # 예를 들어, Django의 기본 User 모델을 사용한다면:

# def create_users(num_users=10000):
#     from django.contrib.auth.models import User
#     for i in range(num_users):
#         username = faker.name()
#         email = f"user{i+1}@example.com"
#         password = f"pass{i+1}"
#         User.objects.create_user(username=username, email=email, password=password)
#         if (i + 1) % 1000 == 0:
#             print(f"👤 {i+1}명의 유저 생성 완료")
#     print("👤 모든 유저 생성 완료.")

# def create_posts():
#     # 가정: 여러분의 프로젝트에 Post 모델이 존재하며, Post는 Movie와 User의 외래키를 갖습니다.
#     # 여기에선 간단히 예시를 들어둡니다.
#     from movies.models import Movie
#     from django.contrib.auth.models import User
#     from myapp.models import Post  # Post 모델이 있는 앱 (예: myapp)로 경로 조정 필요
    
#     users = list(User.objects.all())
#     movies = list(Movie.objects.all())
#     for i in range(10000):
#         user = random.choice(users)
#         movie = random.choice(movies)
#         title = f"{movie.title}에 대한 생각"
#         content = " ".join(random.sample(korean_sentences, 2))
#         Post.objects.create(user=user, movie=movie, title=title, content=content)
#         if i % 1000 == 0:
#             print(f"📝 게시글 {i}개 생성 중...")
#     print("📝 게시글 생성 완료.")

# # 다른 함수들(create_comments, fetch_reviews_and_save, create_review_comments)도
# # 비슷한 방식으로 해당하는 모델과 연결하여 작성할 수 있습니다.

# def run_all():
#     """
#     모든 데이터를 생성하는 함수 (clear_existing_data는 Django ORM으로 대체하는 것이 좋습니다).
#     """
#     # 데이터 삭제: Django ORM을 사용하는 것이 좋으므로 직접 raw SQL 코드 대신 각 모델의 .all().delete()를 쓰십시오.
#     from django.contrib.auth.models import User
#     from myapp.models import Post  # 여러분의 앱 이름과 모델에 맞게 수정
    
#     print("데이터 초기화...")
#     Movie.objects.all().delete()
#     User.objects.all().delete()
#     Post.objects.all().delete()
#     # 다른 관련 모델들도 삭제
#     print("데이터 삭제 완료.")

#     print("영화 데이터 저장...")
#     save_movies(limit=200)
#     print("유저 생성...")
#     create_users(num_users=1000)  # 테스트로 1000명 생성 (숫자 조절 가능)
#     print("게시글 생성...")
#     create_posts()
#     # 댓글, 평론 등 추가 데이터 생성 함수 호출...
#     print("모든 데이터 생성 완료.")

# # 만약 직접 실행하고자 한다면 (Django 커맨드나 쉘에서 호출)
# if __name__ == '__main__':
#     run_all()


# def fetch_movies(page):
#     url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ko-KR&page={page}"
#     #url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&sort_by=release_date.desc&page={page}"
#     response = requests.get(url)
#     data = response.json()
#     if page == 1:
#         print("총 페이지 수:", data.get("total_pages"))
#         print("총 결과 수:", data.get("total_results"))
#     return data.get("results", [])

# if __name__ == "__main__":
#     save_movies(limit=10000)
# movies/utils/fetch_movies.py





# # #영화 데이터 저장
# # # movies/utils/fetch_movies.py

# # import requests
# # import random
# # import time
# # import os
# # import sys
# # import django
# # from faker import Faker

# # # Django settings 설정
# # sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_TeamProject.settings")
# # django.setup()

# # from django.conf import settings
# # from movies.models import Movie

# # faker = Faker('ko_KR')

# # TMDB_API_KEY = getattr(settings, 'TMDB_API_KEY', '133e8ffdf21c352386b08f91ca7054f0')

# # GENRE_MAP_KR = {
# #     28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디", 80: "범죄", 99: "다큐메티리",
# #     18: "드라마", 10751: "가족", 14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
# #     9648: "미스터리", 10749: "로망스", 878: "SF", 10770: "TV 영화", 53: "스리러",
# #     10752: "전쟁", 37: "서부"
# # }

# # def fetch_movies(page):
# #     url = (
# #         f"https://api.themoviedb.org/3/movie/popular?"
# #         f"api_key={TMDB_API_KEY}&language=ko-KR&sort_by=release_date.desc&page={page}"
# #     )
# #     response = requests.get(url)
# #     data = response.json()
# #     return data.get("results", [])

# # def save_movies(limit=500):
# #     saved = 0
# #     normalized_titles = set()

# #     for page in range(1, 1000):  # 충분한 페이지 반복
# #         if saved >= limit:
# #             break

# #         movies = fetch_movies(page)
# #         if not movies:
# #             break

# #         for movie in movies:
# #             if saved >= limit:
# #                 break

# #             title = (movie.get('title') or movie.get('original_title') or '').strip()
# #             if not title:
# #                 continue

# #             norm_title = title.lower()
# #             if norm_title in normalized_titles:
# #                 continue  # 중복 방지

# #             overview = movie.get('overview') or "주력리 정보 없음"
# #             release_date = movie.get('release_date') or None
# #             vote_average = round(movie.get('vote_average', 0), 1)
# #             genre_ids = movie.get('genre_ids', [])
# #             genre_names = [GENRE_MAP_KR.get(gid, f"ID:{gid}") for gid in genre_ids]
# #             genres_str = ", ".join(genre_names)

# #             Movie.objects.create(
# #                 title=title,
# #                 overview=overview,
# #                 release_date=release_date,
# #                 vote_average=vote_average,
# #                 genres=genres_str
# #             )

# #             normalized_titles.add(norm_title)
# #             saved += 1

# #         print(f"🎨 현재까지 저장된 영화 수: {saved}")
# #         time.sleep(0.1)

# #     print(f"🎉 최종 저장 결과: {saved} 개")

# # if __name__ == "__main__":
# #     save_movies(limit=10000)

import os
import sys
import django
import time
import requests
from faker import Faker

# Django 환경 세팅
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_TeamProject.settings")
django.setup()

from django.conf import settings
from movies.models import Movie, Review

faker = Faker('ko_KR')

TMDB_API_KEY = getattr(settings, 'TMDB_API_KEY', '133e8ffdf21c352386b08f91ca7054f0')

GENRE_MAP_KR = {
    28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디",
    80: "범죄", 99: "다큐멘터리", 18: "드라마", 10751: "가족",
    14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
    9648: "미스터리", 10749: "로맨스", 878: "SF", 10770: "TV 영화",
    53: "스릴러", 10752: "전쟁", 37: "서부"
}

def fetch_movies(page):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={page}"
    response = requests.get(url)
    return response.json().get("results", [])

def fetch_reviews(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}&language=ko-KR"
    response = requests.get(url)
    return response.json().get("results", [])

def save_movies(limit=10000):
    saved = 0
    normalized_titles = set(Movie.objects.values_list("title", flat=True))

    for page in range(1, 1000):
        if saved >= limit:
            break

        movies = fetch_movies(page)
        if not movies:
            break

        for movie in movies:
            if saved >= limit:
                break

            title = (movie.get("title") or movie.get("original_title") or "").strip()
            tmdb_id = movie.get("id")
            if not title or not tmdb_id or title.lower() in normalized_titles:
                continue

            overview = movie.get("overview") or "줄거리 정보 없음"
            release_date = movie.get("release_date") or None
            vote_average = round(movie.get("vote_average", 0), 1)
            genre_names = [GENRE_MAP_KR.get(gid, f"ID:{gid}") for gid in movie.get("genre_ids", [])]
            genres_str = ", ".join(genre_names)

            new_movie = Movie.objects.create(
                tmdb_id=tmdb_id,
                title=title,
                overview=overview,
                release_date=release_date,
                vote_average=vote_average,
                genres=genres_str
            )

            normalized_titles.add(title.lower())
            saved += 1

            # 리뷰도 함께 저장
            reviews = fetch_reviews(tmdb_id)
            for review in reviews[:3]:
                content = review.get("content", "").strip()
                if not content:
                    continue
                Review.objects.create(
                    movie=new_movie,
                    author=review.get("author", "익명"),
                    content=content[:500],
                    rating=random.randint(6, 10)
                )

        print(f"🎬 현재까지 저장된 영화 수: {saved}")
        time.sleep(0.1)

    print(f"🎉 최종 저장 결과: {saved}개")

if __name__ == "__main__":
    save_movies(limit=10000)
