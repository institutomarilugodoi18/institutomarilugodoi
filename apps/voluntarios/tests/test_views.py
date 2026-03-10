import pytest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse

from apps.voluntarios.models import Voluntario


@pytest.fixture(autouse=True)
def desabilita_ssl_redirect(settings):
    settings.SECURE_SSL_REDIRECT = False

    
@pytest.fixture
def usuario():
    return User.objects.create_user(
        username="filipe",
        password="123456"
    )


@pytest.fixture
def voluntario():
    return Voluntario.objects.create(
        nome="Maria Silva",
        email="maria@email.com",
        telefone="(12) 99999-9999",
        endereco="Rua A, 123",
        cidade="São José dos Campos",
        area="Evento de adoção",
    )


@pytest.mark.django_db
def test_voluntario_sucesso_retorna_200(client):
    response = client.get(reverse("voluntario_sucesso"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_cadastrar_voluntario_get_com_area_inicial(client):
    response = client.get(reverse("cadastrar_voluntario"), {"area": "Evento de adoção"})

    assert response.status_code == 200
    assert response.context["form"].initial["area"] == "Evento de adoção"


@pytest.mark.django_db
@patch("apps.voluntarios.views.send_mail")
def test_cadastrar_voluntario_post_valido_salva_envia_email_e_redireciona(mock_send_mail, client, settings):
    settings.DEFAULT_FROM_EMAIL = "teste@email.com"
    settings.NOTIFICATIONS_VOLUNTARIOS_TO = ["destino@email.com"]
    settings.EMAIL_FAIL_SILENTLY = True

    dados = {
        "nome": "João Souza",
        "email": "joao@email.com",
        "telefone": "(12) 98888-7777",
        "endereco": "Rua B, 456",
        "cidade": "São José dos Campos",
        "area": "Evento de adoção",
    }

    response = client.post(reverse("cadastrar_voluntario"), dados)

    assert response.status_code == 302
    assert response.url == reverse("voluntario_sucesso")
    assert Voluntario.objects.filter(email="joao@email.com").exists()
    mock_send_mail.assert_called_once()


@pytest.mark.django_db
def test_cadastrar_voluntario_post_invalido_retorna_200_com_erros(client):
    dados = {
        "nome": "",
        "email": "email-invalido",
        "telefone": "(12) 98888-7777",
        "endereco": "Rua B, 456",
        "cidade": "São José dos Campos",
        "area": "Evento de adoção",
    }

    response = client.post(reverse("cadastrar_voluntario"), dados)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors


@pytest.mark.django_db
def test_listar_voluntarios_redireciona_sem_login(client):
    response = client.get(reverse("listar_voluntarios"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_listar_voluntarios_sem_filtros(usuario, voluntario, client):
    client.force_login(usuario)

    response = client.get(reverse("listar_voluntarios"))

    assert response.status_code == 200
    assert response.context["voluntarios_count"] == 1
    assert len(response.context["voluntarios"]) == 1
    assert response.context["cidade_selecionada"] is None
    assert response.context["area_selecionada"] is None


@pytest.mark.django_db
def test_listar_voluntarios_filtra_por_cidade(usuario, client):
    client.force_login(usuario)

    Voluntario.objects.create(
        nome="Maria",
        email="maria1@email.com",
        telefone="(12) 99999-1111",
        endereco="Rua A",
        cidade="São José dos Campos",
        area="Evento de adoção",
    )
    Voluntario.objects.create(
        nome="José",
        email="jose@email.com",
        telefone="(12) 99999-2222",
        endereco="Rua B",
        cidade="Jacareí",
        area="Associado",
    )

    response = client.get(reverse("listar_voluntarios"), {"cidade": "São José dos Campos"})

    assert response.status_code == 200
    assert response.context["cidade_selecionada"] == "São José dos Campos"
    assert response.context["voluntarios_count"] == 1

    voluntarios = response.context["voluntarios"]
    assert voluntarios[0].cidade == "São José dos Campos"


@pytest.mark.django_db
def test_listar_voluntarios_filtra_por_area(usuario, client):
    client.force_login(usuario)

    Voluntario.objects.create(
        nome="Maria",
        email="maria2@email.com",
        telefone="(12) 99999-1111",
        endereco="Rua A",
        cidade="São José dos Campos",
        area="Evento de adoção",
    )
    Voluntario.objects.create(
        nome="José",
        email="jose2@email.com",
        telefone="(12) 99999-2222",
        endereco="Rua B",
        cidade="Jacareí",
        area="Associado",
    )

    response = client.get(reverse("listar_voluntarios"), {"area": "Evento de adoção"})

    assert response.status_code == 200
    assert response.context["area_selecionada"] == "Evento de adoção"
    assert response.context["voluntarios_count"] == 1

    voluntarios = response.context["voluntarios"]
    assert voluntarios[0].area == "Evento de adoção"


@pytest.mark.django_db
def test_login_view_get_retorna_200(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post_valido_redireciona(usuario, client):
    response = client.post(reverse("login"), {
        "username": "filipe",
        "password": "123456",
    })

    assert response.status_code == 302
    assert response.url == reverse("painel")


@pytest.mark.django_db
def test_login_view_post_invalido_exibe_mensagem(client):
    response = client.post(
        reverse("login"),
        {
            "username": "filipe",
            "password": "senha-errada",
        },
        follow=True,
    )

    mensagens = list(get_messages(response.wsgi_request))

    assert response.status_code == 200
    assert any("Usuário ou senha inválidos." in str(m) for m in mensagens)


@pytest.mark.django_db
def test_logout_view_redireciona_para_login(usuario, client):
    client.force_login(usuario)

    response = client.get(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("login")


@pytest.mark.django_db
def test_editar_voluntario_get_retorna_200(usuario, voluntario, client):
    client.force_login(usuario)

    response = client.get(reverse("editar_voluntario", args=[voluntario.id]))

    assert response.status_code == 200
    assert response.context["editar"] is True
    assert response.context["form"].instance == voluntario


@pytest.mark.django_db
def test_editar_voluntario_post_valido_atualiza_e_redireciona(usuario, voluntario, client):
    client.force_login(usuario)

    dados = {
        "nome": "Maria Editada",
        "email": "maria@email.com",
        "telefone": "(12) 97777-7777",
        "endereco": "Rua Nova, 999",
        "cidade": "São José dos Campos",
        "area": "Associado",
    }

    response = client.post(
        reverse("editar_voluntario", args=[voluntario.id]),
        dados
    )

    voluntario.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse("listar_voluntarios")
    assert voluntario.nome == "Maria Editada"
    assert voluntario.area == "Associado"


@pytest.mark.django_db
def test_excluir_voluntario_get_retorna_200(usuario, voluntario, client):
    client.force_login(usuario)

    response = client.get(reverse("excluir_voluntario", args=[voluntario.id]))

    assert response.status_code == 200
    assert response.context["voluntario"] == voluntario


@pytest.mark.django_db
def test_excluir_voluntario_post_exclui_e_redireciona(usuario, voluntario, client):
    client.force_login(usuario)

    response = client.post(
        reverse("excluir_voluntario", args=[voluntario.id]),
        follow=True
    )

    mensagens = list(get_messages(response.wsgi_request))

    assert response.status_code == 200
    assert not Voluntario.objects.filter(id=voluntario.id).exists()
    assert any("foi excluído com sucesso" in str(m) for m in mensagens)