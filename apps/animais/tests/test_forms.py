import io

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.animais.forms import AnimalForm


# ===== FUNÇÕES AUXILIARES =====

def criar_imagem_em_memoria(
    nome="foto.png",
    formato="PNG",
    modo="RGBA",
    tamanho=(2000, 2000),
    cor=(255, 0, 0, 128),
):
    buffer = io.BytesIO()
    imagem = Image.new(modo, tamanho, cor)
    imagem.save(buffer, format=formato)
    buffer.seek(0)

    content_type = f"image/{formato.lower()}"
    return SimpleUploadedFile(
        nome,
        buffer.read(),
        content_type=content_type,
    )


# ===== TESTES DO FORMULÁRIO =====

# Verifica se o formulário configura corretamente os formatos de entrada das datas.
@pytest.mark.django_db
def test_animal_form_configura_input_formats_das_datas():
    form = AnimalForm()

    assert form.fields["data_chegada"].input_formats == ["%Y-%m-%d"]
    assert form.fields["data_saida"].input_formats == ["%Y-%m-%d"]


# Verifica se clean_foto retorna None quando nenhuma foto é enviada.
@pytest.mark.django_db
def test_clean_foto_sem_arquivo_retorna_none():
    form = AnimalForm(
        data={
            "nome": "Mel",
            "descricao": "Sem foto",
            "status": "DISPONIVEL",
            "data_chegada": "2026-03-14",
            "data_saida": "",
        }
    )

    assert form.is_valid() is True
    assert form.cleaned_data["foto"] is None


# Verifica se clean_foto converte imagem RGBA/PNG para JPEG comprimido.
@pytest.mark.django_db
def test_clean_foto_converte_rgba_para_jpg():
    foto = criar_imagem_em_memoria(
        nome="teste.png",
        formato="PNG",
        modo="RGBA",
        tamanho=(2000, 2000),
        cor=(255, 0, 0, 128),
    )

    form = AnimalForm(
        data={
            "nome": "Luna",
            "descricao": "Com foto PNG",
            "status": "DISPONIVEL",
            "data_chegada": "2026-03-14",
            "data_saida": "",
        },
        files={"foto": foto},
    )

    assert form.is_valid() is True

    foto_processada = form.cleaned_data["foto"]
    assert foto_processada is not None
    assert foto_processada.name.endswith(".jpg")
    assert foto_processada.content_type == "image/jpeg"


# Verifica se clean_foto retorna a própria foto quando a compressão não compensa.
@pytest.mark.django_db
def test_clean_foto_retorna_arquivo_original_quando_compressao_nao_compensa(monkeypatch):
    foto = SimpleUploadedFile(
        "pequena.jpg",
        b"arquivo-pequeno",
        content_type="image/jpeg",
    )

    class FakeImage:
        mode = "RGB"

        def thumbnail(self, size):
            pass

        def save(self, output, format, quality, optimize):
            output.write(b"arquivo-maior-do-que-o-original")

    monkeypatch.setattr("apps.animais.forms.Image.open", lambda _: FakeImage())

    form = AnimalForm()
    form.cleaned_data = {"foto": foto}

    resultado = form.clean_foto()

    assert resultado is foto
