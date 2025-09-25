from django.db import models

# Create your models here.
class Voluntario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)  # pode vir do WhatsApp
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=50)
    area = models.CharField(max_length=100)  # área de atuação

    def __str__(self):
        return self.nome
