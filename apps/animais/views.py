from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Animal
from .forms import AnimalForm
import os


@login_required
def lista_animais(request):
    status_selecionado = request.GET.get('status')
    
    # 1. Base total (Todos os animais do banco para os cards e totalizador)
    animais_base = Animal.objects.all()
    total_geral = animais_base.count()

    # 2. Query que será exibida na tabela (com ordenação)
    animais_listagem = animais_base.order_by("-criado_em")

    # 3. Contagens fixas para os Cards (Sempre sobre a base total)
    qtd_disponivel = animais_base.filter(status=Animal.Status.DISPONIVEL).count()
    qtd_adotado = animais_base.filter(status=Animal.Status.ADOTADO).count()
    qtd_tratamento = animais_base.filter(status=Animal.Status.TRATAMENTO).count()

    # 4. Aplicação do Filtro na listagem
    if status_selecionado:
        animais_listagem = animais_listagem.filter(status=status_selecionado)

    # 5. Contagem do que está sendo exibido agora
    animais_count = animais_listagem.count()

    context = {
        "animais": animais_listagem,       # Lista para o loop for
        "animais_count": animais_count,   # Para o "Exibindo X"
        "total_geral": total_geral,       # Para o "de Y"
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
        nome_antigo = animal.foto.name if animal.foto else None
        caminho_antigo = animal.foto.path if animal.foto else None

        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            remover_foto = form.cleaned_data.get("remover_foto")
            nova_foto = request.FILES.get("foto")

            # Caso 1: remover foto atual sem enviar nova
            if remover_foto and not nova_foto and animal.foto:
                animal.foto.delete(save=False)
                animal_salvo = form.save(commit=False)
                animal_salvo.foto = None
                animal_salvo.save(update_fields=["nome", "descricao", "foto", "status", "data_chegada", "data_saida", "atualizado_em"])

                return redirect("animais:lista")
            
            # Caso 2: fluxo normal (mantém ou substitui)
            animal_salvo = form.save()

            # Se enviou nova foto, apaga a antiga do disco
            if nova_foto and nome_antigo and nome_antigo != animal_salvo.foto.name:
                if caminho_antigo and os.path.isfile(caminho_antigo):
                    os.remove(caminho_antigo)

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