import pytest
from django.contrib.auth.models import User

from apps.usuarios.forms import UsuarioCreateForm, UsuarioUpdateForm


pytestmark = pytest.mark.django_db


def test_usuario_create_form_valido():
    form = UsuarioCreateForm(data={
        'username': 'joao',
        'email': 'JOAO@EMAIL.COM',
        'first_name': 'Joao',
        'last_name': 'Silva',
        'password1': 'SenhaForte123',
        'password2': 'SenhaForte123',
        'is_staff': True,
        'is_active': True,
    })

    assert form.is_valid()
    assert form.cleaned_data['email'] == 'joao@email.com'


def test_usuario_create_form_email_duplicado():
    User.objects.create_user(
        username='usuario1',
        email='teste@email.com',
        password='SenhaForte123',
    )

    form = UsuarioCreateForm(data={
        'username': 'usuario2',
        'email': 'TESTE@email.com',
        'first_name': 'Maria',
        'last_name': 'Souza',
        'password1': 'SenhaForte123',
        'password2': 'SenhaForte123',
        'is_staff': False,
        'is_active': True,
    })

    assert not form.is_valid()
    assert 'email' in form.errors
    assert 'Já existe um usuário cadastrado com este e-mail.' in form.errors['email']


def test_usuario_update_form_valido():
    usuario = User.objects.create_user(
        username='joao',
        email='joao@email.com',
        password='SenhaForte123',
    )

    form = UsuarioUpdateForm(
        data={
            'username': 'joao_editado',
            'email': 'JOAO_EDITADO@EMAIL.COM',
            'first_name': 'Joao',
            'last_name': 'Silva',
            'is_staff': True,
            'is_active': True,
        },
        instance=usuario,
    )

    assert form.is_valid()
    assert form.cleaned_data['email'] == 'joao_editado@email.com'


def test_usuario_update_form_email_duplicado_em_outro_usuario():
    User.objects.create_user(
        username='usuario1',
        email='usuario1@email.com',
        password='SenhaForte123',
    )
    usuario2 = User.objects.create_user(
        username='usuario2',
        email='usuario2@email.com',
        password='SenhaForte123',
    )

    form = UsuarioUpdateForm(
        data={
            'username': 'usuario2',
            'email': 'USUARIO1@email.com',
            'first_name': 'Usuario',
            'last_name': 'Dois',
            'is_staff': False,
            'is_active': True,
        },
        instance=usuario2,
    )

    assert not form.is_valid()
    assert 'email' in form.errors
    assert 'Já existe um usuário cadastrado com este e-mail.' in form.errors['email']


def test_usuario_update_form_mesmo_email_do_proprio_usuario():
    usuario = User.objects.create_user(
        username='joao',
        email='joao@email.com',
        password='SenhaForte123',
    )

    form = UsuarioUpdateForm(
        data={
            'username': 'joao',
            'email': 'JOAO@EMAIL.COM',
            'first_name': 'Joao',
            'last_name': 'Silva',
            'is_staff': False,
            'is_active': True,
        },
        instance=usuario,
    )

    assert form.is_valid()
    assert form.cleaned_data['email'] == 'joao@email.com'