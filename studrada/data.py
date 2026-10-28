from datetime import date

COURSES = [
    {
        "slug": "qa-basics",
        "title": "QA: основи тестування",
        "level": "Початковий",
        "teacher": "Олександр Панченко",
        "hours": 24,
        "is_new": True,
        "progress": 60,
        "deadline": date(2026, 11, 20),
        "description": "Що таке якість, тест-кейси, баг-репорти та життєвий цикл дефекту. "
                       "Курс для тих, хто починає шлях у QA.",
        "lessons": [
            {"title": "Що таке QA і навіщо воно потрібне", "minutes": 45,
             "summary": "Якість, QA, QC і тестування: чим вони відрізняються."},
            {"title": "Тест-кейси та чек-листи", "minutes": 60,
             "summary": "Як описати перевірку, щоб її міг повторити будь-хто."},
            {"title": "Баг-репорти", "minutes": 50,
             "summary": "Структура дефекту, серйозність і пріоритет."},
        ],
    },
    {
        "slug": "django-web",
        "title": "Django: веб-розробка",
        "level": "Середній",
        "teacher": "Олександр Панченко",
        "hours": 40,
        "is_new": False,
        "progress": 25,
        "deadline": date(2026, 12, 15),
        "description": "Маршрутизація, представлення, шаблони, моделі та форми. "
                       "Поступово збираємо власний навчальний проєкт.",
        "lessons": [
            {"title": "Маршрутизація та представлення", "minutes": 80,
             "summary": "path(), include(), views, render()."},
            {"title": "Шаблони та статичні файли", "minutes": 80,
             "summary": "Успадкування шаблонів, include, CSS і JavaScript."},
            {"title": "Моделі та ORM", "minutes": 80,
             "summary": "Таблиці як класи Python, запити через QuerySet."},
            {"title": "Форми", "minutes": 80,
             "summary": "Прийом даних від користувача та валідація."},
        ],
    },
    {
        "slug": "sql-postgres",
        "title": "SQL та PostgreSQL",
        "level": "Початковий",
        "teacher": "Олександр Панченко",
        "hours": 20,
        "is_new": False,
        "progress": 100,
        "deadline": None,
        "description": "SELECT, JOIN, DML та транзакції на реальній базі PostgreSQL.",
        "lessons": [
            {"title": "SELECT і фільтрація", "minutes": 70,
             "summary": "WHERE, ORDER BY, LIMIT."},
            {"title": "JOIN", "minutes": 70,
             "summary": "INNER та LEFT JOIN на навчальній схемі LMS."},
        ],
    },
]

STUDENT = {"name": "Олена Коваль", "email": "olena@example.com"}


def get_course(slug):
    """Повертає курс за slug або None."""
    for course in COURSES:
        if course["slug"] == slug:
            return course
    return None