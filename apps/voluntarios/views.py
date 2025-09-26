from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
# Views 1: enviar dados do formulário para o bd
from .forms import VoluntarioForm

def cadastrar_voluntario(request):
    area_selecionada = request.GET.get('area')  # Pega a área da URL

    if request.method == 'POST':
        form = VoluntarioForm(request.POST)
        if form.is_valid():
            voluntario = form.save()
            # Envio de e-mail
            assunto = 'Novo Voluntário Cadastrado'
            corpo = (
                f'O voluntário {voluntario.nome} ({voluntario.email}) '
                f'foi cadastrado com sucesso na área {voluntario.area}!'
            )
            send_mail(
                subject='assunto',
                message=corpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.NOTIFICATIONS_VOLUNTARIOS_TO,
                fail_silently=settings.EMAIL_FAIL_SILENTLY,
            )
            return redirect('voluntario_sucesso')  # redireciona após cadastro
    else:
        form = VoluntarioForm(initial={'area': area_selecionada})
    
    return render(request, 'voluntarios/voluntarios.html', {'form': form})

def voluntario_sucesso(request):
    return render(request, 'voluntarios/sucesso.html')


# Views 2: filtrar dados do bd
from .models import Voluntario
@login_required
def listar_voluntarios(request):
    cidade = request.GET.get('cidade')
    area = request.GET.get('area')

    voluntarios = Voluntario.objects.all()
    voluntarios_count = voluntarios.count()

    if cidade:
        voluntarios = voluntarios.filter(cidade=cidade)

    if area:
        voluntarios = voluntarios.filter(area=area)

    voluntarios_count = voluntarios.count()

    context = {
        'voluntarios': voluntarios,
        'cidade_selecionada': cidade,
        'area_selecionada': area,
        'voluntarios_count': voluntarios_count,
    }

    return render(request, 'voluntarios/listar.html', context)

# Views 3: login e logout
def login_view(request):
    # Limpa mensagens herdadas de redirects anteriores
    if request.method == 'GET':
      list(get_messages(request))  # Consome completamente as mensagens pendentes

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('listar_voluntarios')  # ou outra view após login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'voluntarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # redireciona pra tela de login

@login_required
def editar_voluntario(request, id):
    voluntario = Voluntario.objects.get(id=id)
    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return redirect('listar_voluntarios')
    else:
        form = VoluntarioForm(instance=voluntario)

    return render(request, 'voluntarios/voluntarios.html', {'form': form, 'editar': True})

@login_required
def excluir_voluntario(request, id):
    voluntario = get_object_or_404(Voluntario, id=id)
    
    if request.method == 'POST':
        voluntario.delete()
        messages.success(request, f'Voluntário "{voluntario.nome}" foi excluído com sucesso.')
        return redirect('listar_voluntarios')

    return render(request, 'voluntarios/confirmar_exclusao.html', {'voluntario': voluntario})



# Views 4: consultar dados do bd
''' Alterei listar_volutarios() abaixo pela view 2
def listar_voluntarios(request):
    voluntarios = Voluntario.objects.all().order_by('nome')  # você pode mudar a ordenação depois
    return render(request, 'voluntarios/listar.html', {'voluntarios': voluntarios})
'''