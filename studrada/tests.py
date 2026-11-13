from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Course, CourseReview


class CourseReviewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            slug="python-for-qa",
            title="Python для QA",
            level=Course.Level.BEGINNER,
            teacher="Викладач",
            hours=10,
        )
        self.user = get_user_model().objects.create_user(username="student", password="test-password")
        self.url = f"/lms/{self.course.slug}/review/"

    def test_authenticated_user_can_submit_review(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"rating": "5", "comment": "Дуже корисний курс"})

        self.assertRedirects(response, self.course.get_absolute_url())
        self.assertEqual(CourseReview.objects.get().rating, 5)
        self.assertEqual(CourseReview.objects.get().user, self.user)

    def test_user_updates_existing_review(self):
        CourseReview.objects.create(course=self.course, user=self.user, rating=3, comment="Добре")
        self.client.force_login(self.user)

        self.client.post(self.url, {"rating": "4", "comment": "Стало ще краще"})

        self.assertEqual(CourseReview.objects.count(), 1)
        review = CourseReview.objects.get()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Стало ще краще")

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.post(self.url, {"rating": "5", "comment": "Коментар"})

        self.assertRedirects(response, f"/login/?next={self.url}")
        self.assertEqual(CourseReview.objects.count(), 0)

    def test_rating_outside_range_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"rating": "6", "comment": "Коментар"})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CourseReview.objects.exists())
