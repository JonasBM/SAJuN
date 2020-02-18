from django.urls import path
from juapp import views

urlpatterns = [
    path('', views.start, name='start'),
    path('local/<int:local_id>/', views.local, name='local'),
    path('delete_termo/<int:termo_id>/', views.delete_termo, name='delete_termo'),
    path('force_update/jonas2013/', views.force_update, name='force_update'),
]
