from django.shortcuts import render

from django.views.generic import View, ListView, DetailView
from .models import Courses

class CoursesListView(ListView):
    model = Courses


class CoursesDetailView(DetailView):
    model = Courses


class LessonDetailView(View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course_qs = Courses.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first() #grab the first matching slug

        #get all the lesson associated with course using get_lesson property
        lesson_qs = course.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

            context = {
            'object':lesson
            }

            return render(request , "courses/lesson_detail.html",context)
