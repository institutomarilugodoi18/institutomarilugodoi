from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.animais.models import Animal
from apps.voluntarios.models import Voluntario

@login_required
def dashboard(request):
    # --- Inteligência de Animais ---
    labels_animais = ['Disponíveis', 'Adotados', 'Em Tratamento']
    valores_animais = [
        Animal.objects.filter(status=Animal.Status.DISPONIVEL).count(),
        Animal.objects.filter(status=Animal.Status.ADOTADO).count(),
        Animal.objects.filter(status=Animal.Status.TRATAMENTO).count(),
    ]

    # --- Inteligência de Voluntários ---
    # Pegamos as labels bonitas e as contagens por área
    labels_voluntarios = [choice[1] for choice in Voluntario.Area.choices]
    valores_voluntarios = [
        Voluntario.objects.filter(area=choice[0]).count() 
        for choice in Voluntario.Area.choices
    ]

    context = {
        'labels_animais': labels_animais,
        'valores_animais': valores_animais,
        'labels_voluntarios': labels_voluntarios,
        'valores_voluntarios': valores_voluntarios,
        'total_pets': sum(valores_animais),
        'total_voluntarios': sum(valores_voluntarios),
    }
    
    return render(request, 'relatorios/dashboard.html', context)