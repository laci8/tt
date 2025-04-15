from django.urls import path
from . import views

urlpatterns = [
    path('track-behavior/', views.track_behavior, name='track_behavior'),
    path('track-end/', views.track_end, name='track_end'),

]
