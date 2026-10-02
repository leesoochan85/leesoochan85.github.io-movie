# 🎬 Movie Community

Django와 MariaDB를 기반으로 구현한 **영화 정보 및 커뮤니티 웹 서비스**입니다.

TMDB 기반 영화 데이터를 조회하고 검색할 수 있으며, 영화별 상세 정보와 리뷰를 확인할 수 있습니다.  
회원가입/로그인 기능을 기반으로 게시글 CRUD, 댓글 및 대댓글 기능을 제공합니다.

---

# 🚀 프로그램 실행 방법

## 1. 프로젝트 Clone

```bash
git clone https://github.com/leesoochan85/leesoochan85.github.io-movie.git
```

프로젝트 폴더로 이동합니다.

```bash
cd leesoochan85.github.io-movie
cd 최종파일
```

이후 명령어는 `manage.py`가 있는 `최종파일` 디렉터리에서 실행합니다.

```text
최종파일/
├── manage.py
├── requirements.txt
├── .env.example
├── DB_TeamProject/
├── BoardProject/
├── account/
└── movies/
```

---

## 2. Python 가상환경 생성

```bash
python -m venv venv
```

Windows에서 가상환경 활성화:

```bash
venv\Scripts\activate
```

정상적으로 활성화되면 터미널 앞에 다음과 같이 표시됩니다.

```text
(venv)
```

현재 개발 환경:

```text
Python 3.9
Django 4.2.30
```

---

## 3. 필요한 패키지 설치

프로젝트에 필요한 패키지는 `requirements.txt`에 정의되어 있습니다.

```bash
pip install -r requirements.txt
```

주요 패키지:

```text
Django==4.2.30
mysqlclient==2.2.7
requests==2.32.5
python-dotenv==1.2.1
```

각 패키지의 역할:

| 패키지 | 역할 |
|---|---|
| Django | Web Framework |
| mysqlclient | Django와 MariaDB 연결 |
| requests | TMDB API 요청 |
| python-dotenv | `.env` 환경변수 로딩 |

Django 설치 확인:

```bash
python -m django --version
```

---

# 🔐 4. 환경변수 설정

프로젝트에서는 DB 비밀번호, Django Secret Key, TMDB API Key 등의 민감한 정보를 `.env` 파일로 관리합니다.

GitHub에는 실제 `.env` 파일을 포함하지 않으며 `.env.example`만 제공합니다.

프로젝트 루트의:

```text
.env.example
```

을 참고해:

```text
.env
```

파일을 생성합니다.

예:

```env
TMDB_API_KEY=your_tmdb_api_key

DB_NAME=teamproject
DB_USER=root
DB_PASSWORD=your_mariadb_password
DB_HOST=localhost
DB_PORT=3306

DJANGO_SECRET_KEY=your_django_secret_key
```

실제 API Key 및 비밀번호를 입력합니다.

`.env`는 `.gitignore`에 등록되어 있으므로 GitHub에 업로드되지 않습니다.

---

# 🗄 5. MariaDB 설정

MariaDB 서버를 실행한 뒤 접속합니다.

```bash
mariadb -u root -p
```

또는 환경에 따라:

```bash
mysql -u root -p
```

데이터베이스 목록 확인:

```sql
SHOW DATABASES;
```

`teamproject`가 없다면 생성합니다.

```sql
CREATE DATABASE teamproject
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

확인:

```sql
SHOW DATABASES;
```

종료:

```sql
exit;
```

현재 Django 프로젝트는 다음 MariaDB 데이터베이스를 사용합니다.

```text
Database : teamproject
Host     : localhost
Port     : 3306
```

DB 접속 정보는 `.env`에서 관리합니다.

---

# 🏗 6. Django DB 테이블 생성

MariaDB에 Django 및 프로젝트 테이블을 생성합니다.

```bash
python manage.py migrate
```

다음과 같은 테이블이 생성됩니다.

```text
Django User
Django Session
Movie
Review
Post
Comment
...
```

---

# 🎬 7. 영화 데이터 생성

이 프로젝트의 MariaDB 데이터 자체는 GitHub에 저장하지 않습니다.

따라서 새로운 환경에서는 TMDB API를 통해 영화 데이터를 다시 가져올 수 있도록 Django Management Command를 제공합니다.

TMDB API Key를 `.env`에 설정한 뒤:

```bash
python manage.py fetch_movies
```

를 실행합니다.

구조:

```text
movies/
└── management/
    └── commands/
        └── fetch_movies.py
```

동작 과정:

```text
TMDB API
   ↓
requests
   ↓
fetch_movies
   ↓
Django ORM
   ↓
MariaDB
   ↓
movies_movie
```

이를 통해 `db.sqlite3` 또는 MariaDB 원본 데이터 파일을 GitHub에 직접 업로드하지 않고도 새로운 환경에서 영화 데이터를 구축할 수 있습니다.

> 사용자, 게시글, 댓글 등의 사용자 생성 데이터는 새로운 환경에서 별도로 생성됩니다.

---

# ▶ 8. 서버 실행

```bash
python manage.py runserver
```

정상 실행 시:

```text
Starting development server at http://127.0.0.1:8000/
```

브라우저 접속:

```text
http://127.0.0.1:8000/
```

서버 종료:

```text
Ctrl + C
```

---

# 📌 실행 과정 요약

새로운 PC에서 프로젝트를 실행하는 전체 순서는 다음과 같습니다.

```text
GitHub Clone
      ↓
Python 가상환경 생성
      ↓
pip install -r requirements.txt
      ↓
.env 생성
      ↓
MariaDB teamproject 생성
      ↓
python manage.py migrate
      ↓
python manage.py fetch_movies
      ↓
python manage.py runserver
```

---

# 📌 프로젝트 소개

이 프로젝트는 데이터베이스 설계 및 웹 서비스 구현을 목적으로 개발한 **영화 커뮤니티 웹 애플리케이션**입니다.

주요 기능:

- 영화 목록 조회
- 영화 제목 검색
- 영화 추천
- 영화 상세 정보 조회
- 영화 리뷰 조회
- 회원가입 및 로그인
- 게시글 작성/조회/수정/삭제
- 댓글 작성/수정/삭제
- 대댓글
- 사용자 마이페이지
- 게시글 및 영화 JSON API
- TMDB 영화 데이터 수집
- MariaDB 데이터 관리

Django ORM을 활용해 웹 애플리케이션과 MariaDB를 연동하고 사용자, 영화, 게시글, 댓글 간 관계를 데이터베이스 모델로 구현했습니다.

---

# 🛠 기술 스택

## Backend

- Python 3.9
- Django 4.2.30
- Django ORM

## Database

- MariaDB
- MySQL Client

초기 개발 과정에서는 SQLite를 사용했으며 최종 프로젝트에서는 MariaDB로 이전했습니다.

## Frontend

- HTML
- CSS
- JavaScript
- Django Template

## External API

- TMDB API
- Requests

## Environment

- python-dotenv
- `.env` 기반 환경변수 관리

---

# 📂 프로젝트 구조

```text
최종파일/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
│
├── DB_TeamProject/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── BoardProject/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── migrations/
│   ├── templates/
│   └── static/
│
├── movies/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/
│   ├── templates/
│   ├── utils/
│   └── management/
│       └── commands/
│           └── fetch_movies.py
│
├── account/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│
└── DATABASE/
```

---

# 📂 주요 모듈

## `DB_TeamProject`

Django 프로젝트 전체 설정을 담당합니다.

주요 역할:

- MariaDB 연결
- `.env` 환경변수 로딩
- Django App 등록
- Template 설정
- Static 파일 설정
- URL 진입점 설정
- 로그인/로그아웃 설정

등록된 주요 App:

```python
BoardProject
account
movies
```

---

## `BoardProject`

메인 페이지와 커뮤니티 게시판 기능을 담당합니다.

주요 기능:

- 메인 페이지
- 게시글 목록
- 게시글 작성
- 게시글 상세 조회
- 게시글 수정
- 게시글 삭제
- 댓글
- 대댓글
- 마이페이지
- 게시글 API

---

## `movies`

영화 데이터 관련 기능을 담당합니다.

주요 기능:

- 영화 목록
- 영화 제목 검색
- 영화 상세 정보
- 영화 리뷰
- 평점 기반 추천
- 영화 JSON API
- TMDB 영화 데이터 수집

---

## `account`

사용자 인증 기능을 담당합니다.

주요 기능:

- 로그인
- 로그아웃
- 회원가입
- 비밀번호 변경
- 비밀번호 초기화

Django Authentication 기능을 활용합니다.

---

## `DATABASE`

프로젝트 개발 과정에서 사용한 MariaDB 테이블 설계 및 데이터 관련 코드가 저장되어 있습니다.

---

# 🗄 데이터베이스 구조

## Movie

영화 정보를 저장합니다.

| 필드 | 설명 |
|---|---|
| `tmdb_id` | TMDB 영화 ID |
| `title` | 영화 제목 |
| `overview` | 영화 설명 |
| `release_date` | 개봉일 |
| `vote_average` | 평균 평점 |
| `genres` | 장르 |

---

## Review

영화별 리뷰를 저장합니다.

```text
Movie
 └── Review
```

| 필드 | 설명 |
|---|---|
| `movie` | 대상 영화 |
| `author` | 리뷰 작성자 |
| `content` | 리뷰 내용 |
| `rating` | 리뷰 평점 |

하나의 영화에 여러 리뷰가 연결될 수 있습니다.

---

## Post

커뮤니티 게시글을 저장합니다.

| 필드 | 설명 |
|---|---|
| `title` | 게시글 제목 |
| `content` | 게시글 내용 |
| `writer` | 작성자 |
| `movie` | 관련 영화 |
| `date` | 작성일 |

`User`와 Foreign Key 관계를 가집니다.

```text
User
 └── Post
```

---

## Comment

게시글 댓글을 저장합니다.

| 필드 | 설명 |
|---|---|
| `post` | 게시글 |
| `author` | 작성자 |
| `content` | 댓글 내용 |
| `parent` | 부모 댓글 |
| `created_at` | 작성 시간 |
| `updated_at` | 수정 시간 |

자기 참조 Foreign Key를 활용해 대댓글을 구현했습니다.

```text
Post
 └── Comment
      ├── Reply
      └── Reply
```

---

# 🎬 영화 기능

## 영화 목록

```text
/movies/
```

전체 영화 데이터를 조회합니다.

---

## 영화 검색

```text
/movies/?q=검색어
```

예:

```text
/movies/?q=기생충
```

Django ORM의 `icontains`를 사용합니다.

```python
Movie.objects.filter(title__icontains=query)
```

영화 제목 일부만 입력해도 검색할 수 있습니다.

---

## 영화 추천

평점이 `8.0` 이상인 영화 중 최대 4개를 랜덤으로 선택합니다.

```python
Movie.objects.filter(vote_average__gte=8.0)
```

---

## 영화 상세

```text
/movies/{movie_id}/
```

영화 정보와 해당 영화에 연결된 리뷰를 확인합니다.

---

# 📝 게시판 기능

## 게시글 목록

```text
/list/
```

게시글을 최신순으로 조회합니다.

---

## 게시글 작성

```text
/write/
```

현재 로그인한 사용자가 자동으로 작성자로 저장됩니다.

```python
post.writer = request.user
```

---

## 게시글 상세

```text
/post/{post_id}/
```

게시글 내용과 댓글을 확인합니다.

---

## 게시글 수정

```text
/post/{post_id}/edit/
```

---

## 게시글 삭제

```text
/post/{post_id}/delete/
```

작성자 본인의 게시글만 삭제할 수 있습니다.

---

# 💬 댓글 및 대댓글

댓글 작성:

```text
/post/{post_id}/comment/
```

댓글 수정:

```text
/comment/{comment_id}/edit/
```

댓글 삭제:

```text
/comment/{comment_id}/delete/
```

댓글 모델에 자기 참조 Foreign Key를 적용하여 대댓글 구조를 구현했습니다.

```python
parent = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    related_name='replies'
)
```

---

# 👤 회원 기능

주요 URL:

```text
/login/
/logout/
/register/
/mypage/
```

추가 Django Authentication URL:

```text
/account/login/
/account/logout/
/account/signup/
/account/password_change/
/account/password_reset/
```

---

# 🌐 API

## 게시글 API

```text
/api/posts/
```

게시글 데이터를 JSON 형태로 제공합니다.

---

## 영화 API

```text
/movies/api/
```

검색:

```text
/movies/api/?q=검색어
```

영화 데이터를 JSON 형태로 제공합니다.

---

# 🔄 Django 동작 흐름

```text
Browser
   ↓
DB_TeamProject/urls.py
   ↓
BoardProject/urls.py
   ↓
movies/urls.py
   ↓
movies/views.py
   ↓
Django ORM
   ↓
MariaDB
   ↓
Django Template
   ↓
Browser
```

예:

```text
http://127.0.0.1:8000/movies/10/
```

요청은 `movies.views.movie_detail()`에 전달됩니다.

```python
movie = get_object_or_404(Movie, id=movie_id)
reviews = movie.reviews.all()
```

Django ORM이 MariaDB 데이터를 조회한 후 Template에 전달합니다.

---

# 🔄 SQLite → MariaDB 전환

프로젝트 초기 개발 단계에서는 SQLite를 사용했습니다.

```text
db.sqlite3
```

기존 SQLite에는 다음과 같은 데이터가 저장되어 있었습니다.

```text
Movie   : 10,065
Review  : 20,096
Post    : 6
Comment : 8
User    : 5
```

SQLite 데이터를 Django Fixture 형식으로 추출한 후 MariaDB로 이전했습니다.

```bash
python manage.py dumpdata \
--exclude auth.permission \
--exclude contenttypes \
--indent 2 > sqlite_backup.json
```

MariaDB에 `teamproject` DB를 생성하고:

```bash
python manage.py migrate
```

Fixture 데이터를 로드했습니다.

```bash
python manage.py loaddata sqlite_backup.json
```

총:

```text
30,189 objects
```

가 MariaDB에 정상적으로 이전되었습니다.

최종 프로젝트는 MariaDB를 사용하며 `db.sqlite3` 및 백업 Fixture는 Git 저장소에서 제외합니다.

---

# 🌐 데이터 재구축

MariaDB 자체 데이터 파일은 GitHub에 저장하지 않습니다.

다른 환경에서는 다음 순서로 프로젝트 데이터를 준비할 수 있습니다.

```text
MariaDB teamproject 생성
        ↓
python manage.py migrate
        ↓
python manage.py fetch_movies
        ↓
TMDB에서 영화 데이터 수집
```

이를 통해 특정 PC의 DB 파일에 의존하지 않고 프로젝트를 실행할 수 있도록 구성했습니다.

사용자, 게시글 및 댓글 데이터는 실행 환경에서 새롭게 생성됩니다.

---

# 🔗 주요 URL

| URL | 기능 |
|---|---|
| `/` | 메인 페이지 |
| `/movies/` | 영화 목록 |
| `/movies/?q=` | 영화 검색 |
| `/movies/{id}/` | 영화 상세 |
| `/movies/api/` | 영화 API |
| `/list/` | 게시판 |
| `/write/` | 게시글 작성 |
| `/post/{id}/` | 게시글 상세 |
| `/post/{id}/edit/` | 게시글 수정 |
| `/post/{id}/delete/` | 게시글 삭제 |
| `/post/{id}/comment/` | 댓글 작성 |
| `/comment/{id}/edit/` | 댓글 수정 |
| `/comment/{id}/delete/` | 댓글 삭제 |
| `/login/` | 로그인 |
| `/logout/` | 로그아웃 |
| `/register/` | 회원가입 |
| `/mypage/` | 마이페이지 |
| `/admin/` | Django Admin |
| `/api/posts/` | 게시글 API |

---

# 🔒 환경변수 및 Git 관리

민감한 정보와 로컬 개발 파일은 `.gitignore`를 통해 Git에서 제외합니다.

```gitignore
# Virtual environment
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]

# Environment / secrets
.env
.env.local
.env.production

# DB / backup
db.sqlite3
sqlite_backup.json
db_backup_before_mariadb.sqlite3
db_before_migration.sqlite3

# IDE
.vscode/
.idea/

# OS
Thumbs.db
.DS_Store

# Logs
*.log
```

GitHub에는 실제 `.env` 대신:

```text
.env.example
```

만 제공합니다.

---

# ⚠️ 현재 코드 확인사항

## Django Admin URL 중복

현재 실행 시 다음 warning이 발생할 수 있습니다.

```text
urls.W005
URL namespace 'admin' isn't unique
```

`admin/` URL이 중복 선언되어 있는지 확인하고 하나의 URL 설정으로 정리할 필요가 있습니다.

---

## 게시글 수정 권한 검사

게시글 수정 시 `User` 객체와 username 문자열을 비교하는 코드가 있다면 다음과 같이 수정하는 것이 적절합니다.

```python
if post.writer != request.user:
    return HttpResponseForbidden("수정 권한이 없습니다.")
```

---

## 영화 URL 중복

`BoardProject/urls.py`에서 `movies/` 경로가 중복 선언되어 있다면:

```python
path('movies/', include('movies.urls'))
```

형태로 하나의 진입점으로 통일하는 것이 좋습니다.

---

## 회원가입 Redirect

회원가입 성공 후 존재하지 않는 URL 이름을 사용한다면:

```python
return redirect('main_page')
```

등 실제 URL name에 맞게 수정해야 합니다.

---

# 📌 프로젝트 핵심 학습 내용

이 프로젝트를 통해 다음 내용을 구현하고 학습했습니다.

- Django 프로젝트 구조
- Django MTV 패턴
- Django ORM
- MariaDB 연동
- SQLite → MariaDB 데이터 이전
- Django Migration
- Django Fixture
- 관계형 데이터베이스 설계
- Foreign Key
- 자기 참조 관계
- 회원 인증
- 세션 기반 로그인
- 게시판 CRUD
- 댓글 및 대댓글
- JSON API
- 영화 데이터 검색 및 추천
- TMDB API 연동
- Django Custom Management Command
- `.env` 기반 환경변수 관리
- `requirements.txt` 기반 의존성 관리
- `.gitignore`를 통한 개발 환경 파일 분리
- Template 기반 웹 페이지 구현

---

# 📌 프로젝트 요약

Movie Community는 영화 정보 조회 기능과 커뮤니티 기능을 결합한 Django 기반 웹 서비스입니다.

사용자는 영화 목록을 조회하거나 제목으로 검색할 수 있으며 영화 상세 정보와 리뷰를 확인할 수 있습니다.

회원가입 및 로그인 후 게시글과 댓글을 작성할 수 있으며 자기 참조 Foreign Key를 활용해 대댓글 구조까지 구현했습니다.

초기 SQLite 기반으로 개발한 데이터를 MariaDB로 이전하여 관계형 데이터베이스 환경을 구축했습니다.

또한 DB 파일을 Git 저장소에 직접 포함하는 대신 TMDB API와 Django Management Command를 이용해 새로운 개발 환경에서도 영화 데이터를 다시 구축할 수 있도록 구성했습니다.

환경별 MariaDB 접속 정보, Django Secret Key 및 TMDB API Key는 `.env`로 분리하고 `requirements.txt`를 통해 프로젝트 의존성을 관리하도록 개선했습니다.