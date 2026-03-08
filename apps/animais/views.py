from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Animal
from .forms import AnimalForm

@login_required
def lista_animais(request):
    animais = Animal.objects.all().order_by("-criado_em")
    return render(request, "animais/lista.html", {"animais": animais})

@login_required
def criar_animal(request):
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("animais:lista")
    else:
        form = AnimalForm()

    return render(request, "animais/form.html", {"form": form})