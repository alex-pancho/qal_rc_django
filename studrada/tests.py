from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Course


User = get_user_model()


class CourseApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher",
            password="testpass123"
        )

        self.url = "/api/courses/"

    def test_anonymous_can_read_courses(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_anonymous_cannot_create_course(self):
        data = {
            "title": "Python Automation",
            "slug": "python-automation",
            "level": "beginner",
            "teacher": "Alex",
            "hours": 40
        }

        response = self.client.post(
            self.url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_can_create_course(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Python Automation",
            "slug": "python-automation",
            "level": "beginner",
            "teacher": "Alex",
            "hours": 40
        }

        response = self.client.post(
            self.url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Course.objects.count(),
            1
        )

    def test_create_course_with_token(self):
        token = Token.objects.create(user=self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        data = {
            "title": "Django REST Framework",
            "slug": "django-rest-framework",
            "level": "beginner",
            "teacher": "Alex",
            "hours": 30
        }

        response = self.client.post(
            self.url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

