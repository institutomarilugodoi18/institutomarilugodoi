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

    cidade = forms.ChoiceField(
        choices=Voluntario.Cidade.choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
    )

    area = forms.ChoiceField(
        choices=Voluntario.Area.choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
    )
    
    class Meta:
        model = Voluntario
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'area']
        # Removemos a parte estética do dicionário widgets daqui, 
        # pois o frontend (HTML + widget_tweaks) já cuida disso.