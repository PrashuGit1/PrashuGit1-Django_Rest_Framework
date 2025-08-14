from django.urls import path
from myapp import views

urlpatterns= [
    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),
]