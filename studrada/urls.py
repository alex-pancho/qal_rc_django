from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("", views.lms_home, name="home"),
    path("about/", views.about, name="about"),
    path("studrada/", views.home, name="stud"),
    path("lms/", views.course_list, name="course_list"),
    path("lms/new/", views.course_create, name="course_create"),
    path("lms/<slug:slug>/", views.course_detail, name="course_detail"),
    path("lms/<slug:slug>/review/", views.course_review, name="course_review"),
    path("lms/<slug:slug>/edit/", views.course_update, name="course_update"),
    path("lms/<slug:slug>/lessons/<int:number>/", views.lesson_detail, name="lesson_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reg/", views.register, name="register"),
    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),
]