from django.urls import path
from .views import CoursesListView, CoursesDetailView

app_name = "courses"

urlpatterns = [
    path('', CoursesListView.as_view(), name="List"),
    path('<slug>', CoursesDetailView.as_view(), name="detail"),
]
