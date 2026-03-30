from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    # Dashboard
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

    # Course CRUD
    path("", views.CourseListView.as_view(), name="course_list"),
    path("create/", views.CourseCreateView.as_view(), name="course_create"),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("<slug:slug>/edit/", views.CourseUpdateView.as_view(), name="course_update"),
    path("<slug:slug>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),

    # Enrollment
    path("<slug:slug>/enroll/", views.EnrollView.as_view(), name="enroll"),
    path("<slug:slug>/unenroll/", views.UnenrollView.as_view(), name="unenroll"),

    # Lessons
    path(
        "<slug:course_slug>/lessons/add/",
        views.LessonCreateView.as_view(),
        name="lesson_create",
    ),
    path(
        "<slug:course_slug>/lessons/<int:pk>/",
        views.LessonDetailView.as_view(),
        name="lesson_detail",
    ),
    path(
        "<slug:course_slug>/lessons/<int:pk>/edit/",
        views.LessonUpdateView.as_view(),
        name="lesson_update",
    ),
]
