from django.urls import path
from . import views

app_name = "animais"

urlpatterns = [
    path("", views.lista_animais, name="lista"),
    path("novo/", views.criar_animal, name="criar_animal"),
    path("editar/<int:id>/", views.editar_animal, name="editar_animal"),
    path("excluir/<int:id>/", views.excluir_animal, name="excluir_animal"),
]