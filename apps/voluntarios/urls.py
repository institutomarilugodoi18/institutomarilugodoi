from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastrar_voluntario, name='cadastrar_voluntario'),
    path('sucesso/', views.voluntario_sucesso, name='voluntario_sucesso'),
    path('lista/', views.listar_voluntarios, name='listar_voluntarios'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('editar/<int:id>/', views.editar_voluntario, name='editar_voluntario'),
    path('excluir/<int:id>/', views.excluir_voluntario, name='excluir_voluntario'),
]
