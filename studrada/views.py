from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Course, Lesson
from . forms import TaskForm, CourseForm
from . serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema

class CourseList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        responses=CourseSerializer(many=True),
        summary="Отримати список курсів"
    )
    def get(self, request):
        courses = Course.objects.all()

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)

    @extend_schema(
        request=CourseSerializer,
        responses={201: CourseSerializer},
        summary="Створити новий курс"
    )
    def post(self, request):
        serializer = CourseSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


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
    if course is None:
        raise Http404(f"Курс {slug} не знайдено")
    return render(request, "courses/course_detail.html", {"course": course})

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def course_detail_api(request, pk):
    post = get_object_or_404(Course, pk=pk)

    if request.method == 'GET':
        return Response(CourseSerializer(post).data)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CourseSerializer(
        post,
        data=request.data,
        partial=(request.method == 'PATCH'),
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def lesson_detail(request, slug, number):
    course = get_object_or_404(Course, slug=slug)
    lessons = list(course.lessons.all())

    if not 1 <= number <= len(lessons):
        raise Http404("Урок не знайдено")
    context = {
        "course": course,
        "lesson": lessons[number - 1],
        "number": number,
        "prev_number": number - 1 if number > 1 else None,
        "next_number": number + 1 if number < len(lessons) else None,
    }
    return render(request, "courses/lesson_detail.html", context)


def dashboard(request):
    context = {
        "student": request.user,
        "courses": Course.objects.all(),
    }
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
