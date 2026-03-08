from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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
            return redirect("animais:lista_animais")
    else:
        form = AnimalForm()

    return render(
        request,
        "animais/form.html",
        {"form": form, "titulo": "Cadastrar Animal"},
    )


@login_required
def editar_animal(request, id):
    animal = get_object_or_404(Animal, id=id)

    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            return redirect("animais:lista_animais")
    else:
        form = AnimalForm(instance=animal)

    return render(
        request,
        "animais/form.html",
        {"form": form, "animal": animal, "titulo": "Editar Animal"},
    )


@login_required
def excluir_animal(request, id):
    animal = get_object_or_404(Animal, id=id)

    if request.method == "POST":
        animal.delete()
        return redirect("animais:lista_animais")

    return render(
        request,
        "animais/confirm_delete.html",
        {"animal": animal},
    )