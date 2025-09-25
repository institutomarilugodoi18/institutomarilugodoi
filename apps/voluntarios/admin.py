from django.contrib import admin

# Register your models here.
from .models import Voluntario

# admin.site.register(Voluntario)
@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cidade', 'area')
    search_fields = ('nome', 'email', 'cidade', 'area')
    list_filter = ('cidade', 'area')