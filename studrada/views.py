from django.shortcuts import render
from django.http import HttpResponse, Http404

from . data import COURSES, STUDENT, get_course

def home(request):
    context = {
        "title": "Вітаю!",
        "message": "Сама головна сторінка",
    }

    return render(request, "home.html", context)
# Create your views here.

def custom_404(request, exception):
    return render(request, "base.html", {
        "title": "404  Not found",
    })

def about(request):
    context = {
        "title": "Про себе",
        "message": "Ласкаво просимо до Django!",
    }

    return render(request, "base.html", context)

USERS = {
    "john": {"email": "john@example.com", "role": "admin"},
    "jane": {"email": "jane@example.com", "role": "user"},
    "bob": {"email": "bob@example.com", "role": "moderator"},
}

POSTS = {
    1: {"title": "Перший пост", "content": "Це мій перший пост на блозі."},
    2: {"title": "Другий пост", "content": "Продовжую писати про Django."},
    3: {"title": "Третій пост", "content": "Views та URL-маршрути."},
}


def user_profile(request, username):
    user_info = USERS.get(username)
    if user_info is None:
        raise Http404(f"Користувача {username} не знайдено")

    context = {
        "username": username,
        "email": user_info["email"],
        "role": user_info["role"],
    }
    return render(request, "core/profile.html", context)



def post_detail(request, post_id:int):
    post = POSTS.get(post_id)
    if post is None:
        raise Http404(f"Пост з ID {post_id} не знайдено")
    context = {
        "post_id": post_id,
        "title": post["title"],
        "content": post["content"],
    }
    return render(request, "base.html", {
        "title": context,
    })


def lms_home(request):
    context = {
        "featured": COURSES[:2],
        "courses_count": len(COURSES),
        "lessons_count": sum(len(c["lessons"]) for c in COURSES),
    }
    return render(request, "courses/home.html", context)


def course_list(request):
    query = request.GET.get("q", "").strip()
    courses = COURSES
    if query:
        courses = [c for c in COURSES if query.lower() in c["title"].lower()]
    context = {"courses": courses, "query": query}
    return render(request, "courses/course_list.html", context)


def course_detail(request, slug):
    course = get_course(slug)
    if course is None:
        raise Http404(f"Курс {slug} не знайдено")
    return render(request, "courses/course_detail.html", {"course": course})


def lesson_detail(request, slug, number):
    course = get_course(slug)
    if course is None or not 1 <= number <= len(course["lessons"]):
        raise Http404("Урок не знайдено")
    context = {
        "course": course,
        "lesson": course["lessons"][number - 1],
        "number": number,
        "prev_number": number - 1 if number > 1 else None,
        "next_number": number + 1 if number < len(course["lessons"]) else None,
    }
    return render(request, "courses/lesson_detail.html", context)


def dashboard(request):
    context = {"student": STUDENT, "courses": COURSES}
    return render(request, "courses/dashboard.html", context)