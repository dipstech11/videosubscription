from django.urls import path
from .views import CoursesListView, CoursesDetailView, LessonDetailView

app_name = "courses"

urlpatterns = [
    path('', CoursesListView.as_view(), name="List"),
    path('<slug>', CoursesDetailView.as_view(), name="detail"),
    path('<course_slug>/<lesson_slug>', LessonDetailView.as_view(), name="lesson-detail")
]
