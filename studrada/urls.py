from django.urls import path
from . import views

urlpatterns = [
    path("", views.lms_home, name="home"),
    path("about/", views.about, name="about"),
    path("studrada/", views.home, name="stud"),
    path("lms/", views.course_list, name="course_list"),
    path("lms/<slug:slug>/", views.course_detail, name="course_detail"),
    path("lms/<slug:slug>/lessons/<int:number>/", views.lesson_detail, name="lesson_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
]