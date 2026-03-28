import pytest
from django.contrib.auth.models import User
from django.urls import reverse


pytestmark = pytest.mark.django_db


@pytest.fixture
def usuario_staff():
    return User.objects.create_user(
        username='equipe',
        email='equipe@email.com',
        password='SenhaForte123',
        is_staff=True,
        is_active=True,
    )


@pytest.fixture
def usuario_comum():
    return User.objects.create_user(
        username='comum',
        email='comum@email.com',
        password='SenhaForte123',
        is_staff=False,
        is_active=True,
    )


def test_lista_usuarios_redireciona_sem_login(client):
    response = client.get(reverse('usuarios:lista'))
    assert response.status_code == 302


def test_lista_usuarios_bloqueia_usuario_sem_staff(client, usuario_comum):
    client.login(username='comum', password='SenhaForte123')

    response = client.get(reverse('usuarios:lista'))

    assert response.status_code == 302


def test_lista_usuarios_para_staff(client, usuario_staff):
    User.objects.create_user(
        username='usuario1',
        email='u1@email.com',
        password='SenhaForte123',
        is_active=True,
        is_staff=False,
    )
    User.objects.create_user(
        username='usuario2',
        email='u2@email.com',
        password='SenhaForte123',
        is_active=False,
        is_staff=False,
    )
    User.objects.create_user(
        username='admin',
        email='admin@email.com',
        password='SenhaForte123',
        is_active=True,
        is_staff=True,
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:lista'))

    assert response.status_code == 200
    assert 'usuarios' in response.context
    assert response.context['total_geral'] == 3
    assert response.context['qtd_ativos'] == 2
    assert response.context['qtd_inativos'] == 1
    assert response.context['qtd_staff'] == 1

    usernames = [u.username for u in response.context['usuarios']]
    assert 'admin' not in usernames


def test_lista_usuarios_filtra_ativos(client, usuario_staff):
    ativo = User.objects.create_user(
        username='ativo',
        email='ativo@email.com',
        password='SenhaForte123',
        is_active=True,
    )
    User.objects.create_user(
        username='inativo',
        email='inativo@email.com',
        password='SenhaForte123',
        is_active=False,
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:lista'), {'status': 'ativos'})

    assert response.status_code == 200
    usuarios = list(response.context['usuarios'])
    assert ativo in usuarios
    assert all(u.is_active for u in usuarios)
    assert response.context['status_selecionado'] == 'ativos'


def test_lista_usuarios_filtra_inativos(client, usuario_staff):
    User.objects.create_user(
        username='ativo',
        email='ativo@email.com',
        password='SenhaForte123',
        is_active=True,
    )
    inativo = User.objects.create_user(
        username='inativo',
        email='inativo@email.com',
        password='SenhaForte123',
        is_active=False,
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:lista'), {'status': 'inativos'})

    assert response.status_code == 200
    usuarios = list(response.context['usuarios'])
    assert inativo in usuarios
    assert all(not u.is_active for u in usuarios)
    assert response.context['status_selecionado'] == 'inativos'


def test_lista_usuarios_filtra_staff(client, usuario_staff):
    staff = User.objects.create_user(
        username='staff2',
        email='staff2@email.com',
        password='SenhaForte123',
        is_staff=True,
    )
    User.objects.create_user(
        username='comum2',
        email='comum2@email.com',
        password='SenhaForte123',
        is_staff=False,
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:lista'), {'status': 'staff'})

    assert response.status_code == 200
    usuarios = list(response.context['usuarios'])
    assert staff in usuarios
    assert all(u.is_staff for u in usuarios)
    assert response.context['status_selecionado'] == 'staff'


def test_criar_usuario_get_para_staff(client, usuario_staff):
    client.login(username='equipe', password='SenhaForte123')

    response = client.get(reverse('usuarios:criar'))

    assert response.status_code == 200
    assert response.context['editando'] is False


def test_criar_usuario_post_valido(client, usuario_staff):
    client.login(username='equipe', password='SenhaForte123')

    response = client.post(reverse('usuarios:criar'), data={
        'username': 'novo_usuario',
        'email': 'novo@email.com',
        'first_name': 'Novo',
        'last_name': 'Usuario',
        'password1': 'SenhaForte123',
        'password2': 'SenhaForte123',
        'is_staff': True,
        'is_active': True,
    })

    assert response.status_code == 302
    assert response.url == reverse('usuarios:lista')
    assert User.objects.filter(username='novo_usuario').exists()


def test_criar_usuario_post_invalido(client, usuario_staff):
    client.login(username='equipe', password='SenhaForte123')

    response = client.post(reverse('usuarios:criar'), data={
        'username': '',
        'email': 'email-invalido',
        'password1': '123',
        'password2': '456',
    })

    assert response.status_code == 200
    assert response.context['form'].errors


def test_editar_usuario_get_para_staff(client, usuario_staff):
    usuario = User.objects.create_user(
        username='usuario_editar',
        email='usuario@email.com',
        password='SenhaForte123',
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:editar', args=[usuario.id]))

    assert response.status_code == 200
    assert response.context['editando'] is True
    assert response.context['usuario_obj'] == usuario


def test_editar_usuario_post_valido(client, usuario_staff):
    usuario = User.objects.create_user(
        username='usuario_editar',
        email='usuario@email.com',
        password='SenhaForte123',
        is_staff=False,
        is_active=True,
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.post(reverse('usuarios:editar', args=[usuario.id]), data={
        'username': 'usuario_editado',
        'email': 'editado@email.com',
        'first_name': 'Editado',
        'last_name': 'Silva',
        'is_staff': True,
        'is_active': True,
    })

    usuario.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('usuarios:lista')
    assert usuario.username == 'usuario_editado'
    assert usuario.email == 'editado@email.com'
    assert usuario.is_staff is True


def test_editar_usuario_post_invalido(client, usuario_staff):
    usuario = User.objects.create_user(
        username='usuario_editar',
        email='usuario@email.com',
        password='SenhaForte123',
    )
    User.objects.create_user(
        username='outro',
        email='outro@email.com',
        password='SenhaForte123',
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.post(reverse('usuarios:editar', args=[usuario.id]), data={
        'username': 'usuario_editar',
        'email': 'OUTRO@email.com',
        'first_name': 'Teste',
        'last_name': 'Teste',
        'is_staff': False,
        'is_active': True,
    })

    assert response.status_code == 200
    assert response.context['form'].errors


def test_alternar_status_usuario_inverte_status(client, usuario_staff):
    usuario = User.objects.create_user(
        username='alvo',
        email='alvo@email.com',
        password='SenhaForte123',
        is_active=True,
    )

    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:alternar_status', args=[usuario.id]))

    usuario.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('usuarios:lista')
    assert usuario.is_active is False


def test_alternar_status_usuario_nao_altera_o_proprio_usuario(client, usuario_staff):
    client.login(username='equipe', password='SenhaForte123')
    response = client.get(reverse('usuarios:alternar_status', args=[usuario_staff.id]))

    usuario_staff.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('usuarios:lista')
    assert usuario_staff.is_active is True