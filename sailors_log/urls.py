from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_overview, name='trip_overview'),
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
]
