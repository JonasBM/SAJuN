from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('local/<int:local_id>/', views.local, name='local'),
    path('delete_horario/<int:horario_id>/', views.delete_horario, name='delete_horario'),
]
