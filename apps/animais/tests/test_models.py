import pytest
from unittest.mock import Mock

from apps.animais.models import Animal


# ===== TESTES DE MODELO =====

# Verifica se o método __str__ retorna nome e status formatados corretamente.
@pytest.mark.django_db
def test_str_do_animal_retorna_nome_e_status_formatados():
    animal = Animal.objects.create(
        nome="Mel",
        status=Animal.Status.DISPONIVEL
    )

    assert str(animal) == "Mel (Disponível para Adoção)"


# Verifica se delete remove a foto associada antes de excluir o animal.
@pytest.mark.django_db
def test_delete_do_animal_com_foto_chama_delete_da_foto():
    animal = Animal.objects.create(
        nome="Snoopy",
        status=Animal.Status.DISPONIVEL
    )

    foto_mock = Mock()
    animal.foto = foto_mock

    animal.delete()

    foto_mock.delete.assert_called_once_with(save=False)
