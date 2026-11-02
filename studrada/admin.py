from django.contrib import admin

from . models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

# admin.site.register(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "teacher", "hours", "is_new")
    list_filter = ("level", "is_new")
    search_fields = ("title", "teacher")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]
