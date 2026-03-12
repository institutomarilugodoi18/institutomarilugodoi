from django import forms
from .models import Voluntario

class VoluntarioForm(forms.ModelForm):
    # Mantemos o honeypot aqui, pois é um campo extra (não está no banco)
    website = forms.CharField(
        required=False,
        label='Deixe em branco',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'tabindex': '-1',
        })
    )
    
    class Meta:
        model = Voluntario
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'area']
        # Removemos o dicionário widgets daqui, 
        # pois o frontend (HTML + widget_tweaks) já cuida disso.