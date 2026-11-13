from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Avg
from . models import Course, CourseReview, Lesson
from . forms import TaskForm, CourseForm, CourseReviewForm


def task_create(request):
    form = TaskForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        print(title, description)

    return render(request, "courses/task_form.html", {"form": form})


def course_create(request):
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        course = Course.objects.create(**form.cleaned_data)
        # messages.success(request, f"Курс «{course.title}» створено.")
        return redirect("course_detail", slug=course.slug)
    else:
        form = CourseForm()
    return render(request, "courses/course_form.html", {"form": form})

@permission_required(
    "studrada.change_course"
)
def course_update(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect(course)
    else:
        form = CourseForm(instance=course)
    context = {"form": form, "heading": f"Редагувати: {course.title}"}
    return render(request, "courses/course_form.html", context)


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
        "featured": Course.objects.all()[:2],
        "courses_count": Course.objects.count(),
        "lessons_count": Lesson.objects.count(),
    }
    return render(request, "courses/home.html", context)


def course_list(request):
    query = request.GET.get("q", "").strip()
    courses = Course.objects.all()
    if query:
        courses = courses.filter(title__icontains=query)
    context = {"courses": courses, "query": query}
    return render(request, "courses/course_list.html", context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    review = CourseReview.objects.filter(course=course, user=request.user).first() if request.user.is_authenticated else None
    form = CourseReviewForm(instance=review)
    context = {
        "course": course,
        "reviews": course.reviews.select_related("user").all(),
        "average_rating": course.reviews.aggregate(average=Avg("rating"))["average"],
        "review_form": form,
        "user_review": review,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def course_review(request, slug):
    course = get_object_or_404(Course, slug=slug)
    review = CourseReview.objects.filter(course=course, user=request.user).first()
    form = CourseReviewForm(request.POST, instance=review)
    if form.is_valid():
        saved_review = form.save(commit=False)
        saved_review.course = course
        saved_review.user = request.user
        saved_review.save()
        return redirect(course)
    context = {
        "course": course,
        "reviews": course.reviews.select_related("user").all(),
        "average_rating": course.reviews.aggregate(average=Avg("rating"))["average"],
        "review_form": form,
        "user_review": review,
    }
    return render(request, "courses/course_detail.html", context)


def lesson_detail(request, slug, number):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, course=course, order=number)
    lesson_count = course.lessons.count()
    context = {
        "course": course,
        "lesson": lesson,
        "number": number,
        "prev_number": number - 1 if number > 1 else None,
        "next_number": number + 1 if number < lesson_count else None,
    }
    return render(request, "courses/lesson_detail.html", context)


def dashboard(request):
    from .data import COURSES, STUDENT

    context = {"student": STUDENT, "courses": COURSES}
    return render(request, "courses/dashboard.html", context)


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )
