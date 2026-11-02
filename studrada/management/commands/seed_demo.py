from django.core.management.base import BaseCommand

from studrada.data import COURSES
from studrada.models import Course

LEVELS = {"Початковий": "beginner", "Середній": "intermediate", "Просунутий": "advanced"}


class Command(BaseCommand):
    help = "Заповнює базу демо-даними з courses/data.py (можна запускати повторно)"

    def handle(self, *args, **options):
        created = updated = 0
        for item in COURSES:
            course, was_created = Course.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "level": LEVELS[item["level"]],
                    "teacher": item["teacher"],
                    "hours": item["hours"],
                    "is_new": item["is_new"],
                    "description": item["description"],
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Курси: створено {created}, оновлено {updated}"))
