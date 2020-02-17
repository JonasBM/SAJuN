from django.urls import path
from juapp import views

urlpatterns = [
    path('', views.start, name='start'),
    path('local/<int:local_id>/', views.local, name='local'),
    path('delete_termo/<int:termo_id>/', views.delete_termo, name='delete_termo'),
]
