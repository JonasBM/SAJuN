from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('local/<int:local_id>/', views.local, name='local'),
]
