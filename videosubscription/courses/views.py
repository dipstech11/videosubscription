from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Courses

class CoursesListView(ListView):
    model = Courses



class CoursesDetailView(DetailView):
    model = Courses
