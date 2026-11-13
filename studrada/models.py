from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse 
# from django.contrib import admin

class Course(models.Model): # class BookAdmin(admin.ModelAdmin):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Початковий"
        INTERMEDIATE = "intermediate", "Середній"
        ADVANCED = "advanced", "Просунутий"

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    teacher = models.CharField(max_length=100)
    hours = models.PositiveSmallIntegerField()
    is_new = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    minutes = models.PositiveSmallIntegerField()
    summary = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_lesson_order_per_course"),
        ]

    def __str__(self):
        return f"{self.course.title}: {self.order}. {self.title}"


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["course", "user"], name="unique_review_per_user_course"),
            models.CheckConstraint(condition=Q(rating__gte=1, rating__lte=5), name="course_review_rating_1_to_5"),
        ]

    def __str__(self):
        return f"{self.user} - {self.course} ({self.rating}/5)"
