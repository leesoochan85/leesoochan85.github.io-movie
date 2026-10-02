import os
import sys
import django

# Django 환경 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_TeamProject.settings")
django.setup()

from django.contrib.auth.models import User
from board.models import Post

def fix_null_writers():
    # "탈퇴한 사용자" 유저가 없다면 생성
    retired_user, created = User.objects.get_or_create(username='탈퇴한 사용자')
    if created:
        retired_user.set_password('retired1234')
        retired_user.save()
        print("✅ '탈퇴한 사용자' 유저 생성 완료")
    else:
        print("ℹ️ 이미 존재하는 '탈퇴한 사용자' 유저 사용")

    # writer가 None인 게시글 업데이트
    updated = Post.objects.filter(writer=None).update(writer=retired_user)
    print(f"🔧 {updated}개의 게시글의 작성자를 '탈퇴한 사용자'로 변경 완료")

if __name__ == "__main__":
    fix_null_writers()