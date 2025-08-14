from django.urls import path
from .views import student_list, student_detail

urlpatterns = [
    path('students/', student_list),          # List & Create
    path('students/<int:pk>/', student_detail), # Retrieve, Update, Delete
]
