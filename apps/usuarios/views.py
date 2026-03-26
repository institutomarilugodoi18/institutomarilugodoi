from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UsuarioCreateForm, UsuarioUpdateForm


def usuario_equipe(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(usuario_equipe)
def lista_usuarios(request):
    status_selecionado = request.GET.get('status', '').strip()

    usuarios = User.objects.all().order_by('username')

    if status_selecionado == 'ativos':
        usuarios = usuarios.filter(is_active=True)
    elif status_selecionado == 'inativos':
        usuarios = usuarios.filter(is_active=False)
    elif status_selecionado == 'staff':
        usuarios = usuarios.filter(is_staff=True)

    total_geral = User.objects.count()
    qtd_ativos = User.objects.filter(is_active=True).count()
    qtd_inativos = User.objects.filter(is_active=False).count()
    qtd_staff = User.objects.filter(is_staff=True).count()

    context = {
        'usuarios': usuarios,
        'usuarios_count': usuarios.count(),
        'total_geral': total_geral,
        'qtd_ativos': qtd_ativos,
        'qtd_inativos': qtd_inativos,
        'qtd_staff': qtd_staff,
        'status_selecionado': status_selecionado,
    }

    return render(request, 'usuarios/lista_usuarios.html', context)


@login_required
@user_passes_test(usuario_equipe)
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista')
    else:
        form = UsuarioCreateForm()

    context = {
        'form': form,
        'editando': False,
    }
    return render(request, 'usuarios/form_usuarios.html', context)


@login_required
@user_passes_test(usuario_equipe)
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista')
    else:
        form = UsuarioUpdateForm(instance=usuario)

    context = {
        'form': form,
        'editando': True,
        'usuario_obj': usuario,
    }
    return render(request, 'usuarios/form_usuarios.html', context)


@login_required
@user_passes_test(usuario_equipe)
def alternar_status_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if usuario != request.user:
        usuario.is_active = not usuario.is_active
        usuario.save()

    return redirect('usuarios:lista')