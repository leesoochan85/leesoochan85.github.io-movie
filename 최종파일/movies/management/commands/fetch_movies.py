import os
import requests

from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = "TMDB API에서 영화 데이터를 수집합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--pages",
            type=int,
            default=10,
            help="수집할 TMDB 페이지 수",
        )

    def handle(self, *args, **options):
        api_key = os.environ.get("TMDB_API_KEY")

        if not api_key:
            self.stderr.write(
                self.style.ERROR("TMDB_API_KEY가 설정되어 있지 않습니다.")
            )
            return

        pages = options["pages"]

        for page in range(1, pages + 1):
            url = "https://api.themoviedb.org/3/movie/popular"

            params = {
                "api_key": api_key,
                "language": "ko-KR",
                "page": page,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            movies = response.json().get("results", [])

            for data in movies:
                Movie.objects.update_or_create(
                    tmdb_id=data["id"],
                    defaults={
                        "title": data.get("title", ""),
                        "overview": data.get("overview", ""),
                        "release_date": data.get("release_date") or None,
                        "vote_average": data.get("vote_average", 0),
                    },
                )

            self.stdout.write(
                self.style.SUCCESS(f"{page}/{pages} 페이지 저장 완료")
            )

        self.stdout.write(
            self.style.SUCCESS("영화 데이터 수집 완료")
        )