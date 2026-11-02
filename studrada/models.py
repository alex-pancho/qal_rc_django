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
