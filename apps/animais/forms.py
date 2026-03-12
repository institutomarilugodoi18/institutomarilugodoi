from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["nome", "descricao", "foto", "status", "data_chegada", "data_saida"]
        # Deixamos o HTML gerenciar as classes via add_class para manter o padrão profissional
        #widgets = {
        #    "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do animal"}),
        #    "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Observações / descrição"}),
        #    "status": forms.Select(attrs={"class": "form-select"}),
        #    "data_chegada": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        #    "data_saida": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        #}