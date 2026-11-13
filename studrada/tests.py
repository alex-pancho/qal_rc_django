from django.test import TestCase
from django.urls import reverse

from .models import Course, Lesson


class CoursePagesTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            slug="django-basics",
            title="Основи Django",
            teacher="Викладач",
            hours=4,
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Перший урок",
            minutes=30,
            order=1,
        )

    def test_course_pages_use_database_records(self):
        home = self.client.get(reverse("home"))
        course_list = self.client.get(reverse("course_list"), {"q": "django"})
        course_detail = self.client.get(reverse("course_detail", args=[self.course.slug]))
        lesson_detail = self.client.get(
            reverse("lesson_detail", args=[self.course.slug, self.lesson.order])
        )

        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "1")
        self.assertContains(course_list, self.course.title)
        self.assertContains(course_detail, self.lesson.title)
        self.assertContains(lesson_detail, self.lesson.title)

    def test_dashboard_uses_database_courses_and_current_user(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)
        self.assertContains(response, "data-lesson-orders=\"1\"")
