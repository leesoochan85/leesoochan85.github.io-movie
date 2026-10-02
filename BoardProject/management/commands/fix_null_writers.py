from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from BoardProject.models import Post

class Command(BaseCommand):
    help = 'writer가 None인 게시글을 탈퇴한 사용자로 지정합니다.'

    def handle(self, *args, **options):
        retired_user, created = User.objects.get_or_create(username='탈퇴한 사용자')
        if created:
            retired_user.set_password('retired1234')
            retired_user.save()
            self.stdout.write("✅ '탈퇴한 사용자' 유저 생성 완료")
        else:
            self.stdout.write("ℹ️ 이미 존재하는 '탈퇴한 사용자' 유저 사용")

        updated = Post.objects.filter(writer=None).update(writer=retired_user)
        self.stdout.write(f"🔧 {updated}개의 게시글의 작성자를 '탈퇴한 사용자'로 변경 완료")
