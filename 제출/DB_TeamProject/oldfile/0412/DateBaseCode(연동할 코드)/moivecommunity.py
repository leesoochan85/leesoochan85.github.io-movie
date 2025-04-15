// pip install requests pymysql Faker(파이썬에서 코드 실행전 설치해야 하는 패키지)
// api키로 영화 정보를 받고 랜덤으로 데이터 생성 및 sql에 연동하는 코드입니다.

import requests
import pymysql
from faker import Faker
import random
import time

faker = Faker('ko_KR')
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

API_KEY = '133e8ffdf21c352386b08f91ca7054f0'

GENRE_MAP_KR = {
    28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디", 80: "범죄", 99: "다큐멘터리",
    18: "드라마", 10751: "가족", 14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
    9648: "미스터리", 10749: "로맨스", 878: "SF", 10770: "TV 영화", 53: "스릴러",
    10752: "전쟁", 37: "서부"
}

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root@1234',
    db='test',
    charset='utf8mb4'
)
cursor = conn.cursor()

def clear_existing_data():
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE comments;")
    cursor.execute("TRUNCATE TABLE posts;")
    cursor.execute("TRUNCATE TABLE users;")
    cursor.execute("TRUNCATE TABLE movies;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()
    print("🧹 기존 데이터 삭제 완료")

def fetch_movies(page):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ko-KR&sort_by=release_date.desc&page={page}"
    response = requests.get(url)
    return response.json().get("results", [])

def save_movies(limit=200):
    saved = 0
    for page in range(1, 11):
        if saved >= limit:
            break
        movies = fetch_movies(page)
        for movie in movies:
            if saved >= limit:
                break
            title = movie.get('title') or movie.get('original_title')
            if not title:
                continue
            overview = movie.get('overview') or "줄거리 정보 없음"
            release_date = movie.get('release_date')
            vote_average = round(movie.get('vote_average', 0), 1)
            genre_names = [GENRE_MAP_KR.get(gid, f"ID:{gid}") for gid in movie.get('genre_ids', [])]
            genres_str = ", ".join(genre_names)

            cursor.execute("""
                INSERT INTO movies (title, overview, release_date, vote_average, genres)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, overview, release_date, vote_average, genres_str))
            saved += 1
        conn.commit()
        print(f"🎬 저장된 영화 수: {saved}")
        time.sleep(0.1)

def create_users(num_users=10000):
    for i in range(num_users):
        username = faker.name()
        email = f"user{i+1}@example.com"
        password = f"pass{i+1}"
        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """, (username, email, password))
        if (i + 1) % 1000 == 0:
            conn.commit()
            print(f"👤 {i+1}명 유저 생성 완료")
    conn.commit()

def create_posts():
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id, title FROM movies")
    movies = cursor.fetchall()

    for i, user_id in enumerate(user_ids[:10000]):
        movie_id, movie_title = random.choice(movies)
        title = f"{movie_title}에 대한 생각"
        content = " ".join(random.sample(korean_sentences, 2))
        cursor.execute("""
            INSERT INTO posts (user_id, movie_id, title, content)
            VALUES (%s, %s, %s, %s)
        """, (user_id, movie_id, title, content))
        if i % 1000 == 0:
            conn.commit()
            print(f"📝 게시글 {i}개 생성 완료")
    conn.commit()

def create_comments():
    cursor.execute("SELECT id FROM posts")
    post_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    total_comments = 0
    all_comment_ids = []

    for post_id in post_ids:
        num_comments = random.randint(1, 2)
        current_comment_ids = []

        for _ in range(num_comments):
            user_id = random.choice(user_ids)
            content = random.choice(korean_sentences)
            cursor.execute("""
                INSERT INTO comments (post_id, user_id, content, parent_comment_id)
                VALUES (%s, %s, %s, NULL)
            """, (post_id, user_id, content))
            comment_id = cursor.lastrowid
            current_comment_ids.append(comment_id)
            all_comment_ids.append(comment_id)
            total_comments += 1

        for parent_id in current_comment_ids:
            user_id = random.choice(user_ids)
            content = "↪ " + random.choice(korean_sentences)
            cursor.execute("""
                INSERT INTO comments (post_id, user_id, content, parent_comment_id)
                VALUES (%s, %s, %s, %s)
            """, (post_id, user_id, content, parent_id))
            child_id = cursor.lastrowid
            all_comment_ids.append(child_id)
            total_comments += 1

    conn.commit()
    print(f"✅ 총 {total_comments}개 댓글/대댓글 생성 완료")

if __name__ == "__main__":
    clear_existing_data()
    save_movies(limit=200)
    create_users(10000)
    create_posts()
    create_comments()
    cursor.close()
    conn.close()
    print("🎉 모든 데이터 생성 완료!")
