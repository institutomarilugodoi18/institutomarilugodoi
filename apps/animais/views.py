from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Animal
from .forms import AnimalForm


@login_required
def lista_animais(request):
    status_selecionado = request.GET.get('status')
    animais = Animal.objects.all().order_by("-criado_em")

    # Contagens para os Cards de Resumo
    total_geral = animais.count()
    qtd_disponivel = animais.filter(status="DISPONIVEL").count()
    qtd_adotado = animais.filter(status="ADOTADO").count()
    qtd_tratamento = animais.filter(status="TRATAMENTO").count()

    # Aplicação do Filtro
    if status_selecionado:
        animais = animais.filter(status=status_selecionado)

    context = {
        "animais": animais,
        "total_geral": total_geral,
        "qtd_disponivel": qtd_disponivel,
        "qtd_adotado": qtd_adotado,
        "qtd_tratamento": qtd_tratamento,
        "status_selecionado": status_selecionado,
        "Status": Animal.Status, 
    }
    return render(request, "animais/lista.html", context)

@login_required
def criar_animal(request):
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("animais:lista")
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
            return redirect("animais:lista")
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
        return redirect("animais:lista")

    return render(
        request,
        "animais/confirm_delete.html",
        {"animal": animal},
    )