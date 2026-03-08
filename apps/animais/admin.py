from django.contrib import admin

# Register your models here.
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("nome", "status", "data_chegada", "data_saida", "criado_em")
    list_filter = ("status", "data_chegada", "data_saida")
    search_fields = ("nome", "descricao")
    ordering = ("-criado_em",)