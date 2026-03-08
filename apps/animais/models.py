from django.db import models

# Create your models here.
class Animal(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = "DISPONIVEL", "Disponível"
        ADOTADO = "ADOTADO", "Adotado"

    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)

    # Foto vai existir, mas o upload só funciona quando configurarmos MEDIA_*
    foto = models.ImageField(upload_to="animais/fotos/", blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DISPONIVEL,
    )

    data_chegada = models.DateField(blank=True, null=True)
    data_saida = models.DateField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.nome} ({self.get_status_display()})"