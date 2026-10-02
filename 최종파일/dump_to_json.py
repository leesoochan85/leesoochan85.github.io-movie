# dump_to_json.py
import io
import sys
from django.core.management import call_command
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_TeamProject.settings")
django.setup()

with io.open('data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', '--exclude=auth.permission', '--exclude=contenttypes', indent=2, stdout=f)

print("✅ 데이터가 data.json 파일로 저장되었습니다.")
