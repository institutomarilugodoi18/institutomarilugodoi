from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]