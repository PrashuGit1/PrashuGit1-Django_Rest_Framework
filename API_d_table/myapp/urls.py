from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customer_list),
    path('customers/<int:pk>/', views.customer_detail),

    path('orders/', views.order_list),
    path('orders/<int:pk>/', views.order_detail),
]
