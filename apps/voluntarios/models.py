from django.db import models

class Voluntario(models.Model):
    class Cidade(models.TextChoices):
        SJC = "São José dos Campos", "São José dos Campos"
        JACAREI = "Jacareí", "Jacareí"
        CACAPAVA = "Caçapava", "Caçapava"
        TAUBATE = "Taubaté", "Taubaté"

    class Area(models.TextChoices):
        ADOCAO = "Evento de adoção", "Evento de Adoção"
        CUIDADOS = "Cuidados e Bem-Estar", "Cuidados e Bem-Estar"
        ASSOCIADO = "Associado", "Associado"
        OUTRAS = "Outras tarefas", "Outras Tarefas"

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    
    # Agora usando choices para garantir integridade
    cidade = models.CharField(
        max_length=50, 
        choices=Cidade.choices
    )
    area = models.CharField(
        max_length=100, 
        choices=Area.choices
    )

    def __str__(self):
        return self.nome