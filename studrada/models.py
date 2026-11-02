from django.db import models


class Course(models.Model):
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

