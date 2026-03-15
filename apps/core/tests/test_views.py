import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def usuario():
    return User.objects.create_user(
        username="filipe",
        password="123456"
    )


@pytest.mark.django_db
def test_usuario_logado_acessa_painel_e_retorna_200(client, usuario):
    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.get(reverse("core:painel"))

    assert response.status_code == 200