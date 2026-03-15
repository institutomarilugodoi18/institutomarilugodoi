import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.animais.models import Animal


# ===== FIXTURES =====

# Cria um usuário para os testes de autenticação. O usuário é criado no banco de dados e pode ser utilizado para realizar login durante os testes.
@pytest.fixture
def usuario():
    return User.objects.create_user(
        username="filipe",
        password="123456"
    )


# ===== TESTES DE LISTAGEM =====

# Verifica se usuário logado acessa a lista de animais e recebe status 200.
@pytest.mark.django_db
def test_usuario_logado_acessa_lista_animais_e_retorna_200(client, usuario):
    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.get(reverse("animais:lista"))

    assert response.status_code == 200


# Verifica se a lista de animais filtra corretamente por status.
@pytest.mark.django_db
def test_lista_animais_filtra_por_status(client, usuario):
    Animal.objects.create(nome="Mel", status=Animal.Status.DISPONIVEL)
    Animal.objects.create(nome="Bob", status=Animal.Status.ADOTADO)
    Animal.objects.create(nome="Luna", status=Animal.Status.TRATAMENTO)

    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.get(reverse("animais:lista"), {"status": Animal.Status.DISPONIVEL})

    assert response.status_code == 200

    animais = response.context["animais"]
    assert animais.count() == 1
    assert animais.first().nome == "Mel"
    assert animais.first().status == Animal.Status.DISPONIVEL



# ===== TESTES DE CRIAÇÃO =====

# Verifica se usuário logado acessa o formulário de criação de animal via GET.
@pytest.mark.django_db
def test_usuario_logado_acessa_form_criar_animal(client, usuario):
    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.get(reverse("animais:criar_animal"))

    assert response.status_code == 200


# Verifica se usuário logado cria um animal com dados básicos e sem foto.
@pytest.mark.django_db
def test_usuario_logado_cria_animal_com_dados_basicos(client, usuario):
    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.post(reverse("animais:criar_animal"), {
        "nome": "Snoopy",
        "descricao": "Cachorro dócil e brincalhão",
        "status": Animal.Status.DISPONIVEL,
        "data_chegada": "2026-03-14",
        "data_saida": "",
    })

    assert response.status_code == 302
    assert Animal.objects.count() == 1

    animal = Animal.objects.first()
    assert animal.nome == "Snoopy"
    assert animal.descricao == "Cachorro dócil e brincalhão"
    assert animal.status == Animal.Status.DISPONIVEL
    assert str(animal.data_chegada) == "2026-03-14"
    assert animal.foto in [None, ""]


# Verifica se POST inválido não cria animal e mantém o formulário na tela.
@pytest.mark.django_db
def test_post_invalido_nao_cria_animal(client, usuario):
    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.post(reverse("animais:criar_animal"), {
        "nome": "",
        "descricao": "Teste sem nome",
        "status": Animal.Status.DISPONIVEL,
        "data_chegada": "2026-03-14",
        "data_saida": "",
    })

    assert response.status_code == 200
    assert Animal.objects.count() == 0


# ===== TESTES DE EDIÇÃO =====

# Verifica se usuário logado acessa o formulário de edição de um animal existente.
@pytest.mark.django_db
def test_usuario_logado_acessa_form_editar_animal(client, usuario):
    animal = Animal.objects.create(
        nome="Mel",
        status=Animal.Status.DISPONIVEL
    )

    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.get(reverse("animais:editar_animal", args=[animal.id]))

    assert response.status_code == 200


# Verifica se usuário logado edita com sucesso os dados de um animal existente.
@pytest.mark.django_db
def test_usuario_logado_edita_animal_com_sucesso(client, usuario):
    animal = Animal.objects.create(
        nome="Mel",
        descricao="Descrição antiga",
        status=Animal.Status.DISPONIVEL
    )

    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.post(reverse("animais:editar_animal", args=[animal.id]), {
        "nome": "Mel Atualizada",
        "descricao": "Descrição nova",
        "status": Animal.Status.ADOTADO,
        "data_chegada": "2026-03-14",
        "data_saida": "2026-03-15",
        "remover_foto": "",
    })

    assert response.status_code == 302

    animal.refresh_from_db()
    assert animal.nome == "Mel Atualizada"
    assert animal.descricao == "Descrição nova"
    assert animal.status == Animal.Status.ADOTADO
    assert str(animal.data_chegada) == "2026-03-14"
    assert str(animal.data_saida) == "2026-03-15"


# Verifica se usuário logado remove a foto atual de um animal durante a edição.
@pytest.mark.django_db
def test_usuario_logado_remove_foto_do_animal_na_edicao(client, usuario):
    from apps.animais.tests.test_forms import criar_imagem_em_memoria

    foto = criar_imagem_em_memoria(
        nome="foto.png",
        formato="PNG",
        modo="RGBA",
        tamanho=(300, 300),
        cor=(255, 0, 0, 128),
    )

    animal = Animal.objects.create(
        nome="Mel",
        descricao="Com foto",
        status=Animal.Status.DISPONIVEL,
        foto=foto,
    )

    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.post(reverse("animais:editar_animal", args=[animal.id]), {
        "nome": "Mel",
        "descricao": "Sem foto agora",
        "status": Animal.Status.DISPONIVEL,
        "data_chegada": "",
        "data_saida": "",
        "remover_foto": "on",
    })

    assert response.status_code == 302

    animal.refresh_from_db()
    assert animal.foto in [None, ""]


# ===== TESTES DE EXCLUSÃO =====

# Verifica se usuário logado acessa a tela de confirmação de exclusão de um animal.
@pytest.mark.django_db
def test_usuario_logado_acessa_confirmacao_excluir_animal(client, usuario):
    animal = Animal.objects.create(
        nome="Snoopy",
        status=Animal.Status.DISPONIVEL
    )

    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.get(reverse("animais:excluir_animal", args=[animal.id]))

    assert response.status_code == 200
    assert response.context["animal"] == animal


# Verifica se usuário logado exclui com sucesso um animal existente.
@pytest.mark.django_db
def test_usuario_logado_exclui_animal_com_sucesso(client, usuario):
    animal = Animal.objects.create(
        nome="Snoopy",
        status=Animal.Status.DISPONIVEL
    )

    login = client.login(username="filipe", password="123456")
    assert login is True

    response = client.post(reverse("animais:excluir_animal", args=[animal.id]))

    assert response.status_code == 302
    assert Animal.objects.filter(id=animal.id).count() == 0
