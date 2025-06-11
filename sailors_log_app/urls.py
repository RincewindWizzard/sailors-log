from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:pk>/weather', views.trip_weather_statistics, name='trip_weather'),
    path('trip/new/', views.create_trip, name='trip_create'),
    path('trip/<int:pk>/delete/', views.trip_delete, name='trip_delete'),
    path('stats/boat_statistics/', views.boat_statistics, name='boat_statistics'),
]
