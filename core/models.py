from django.db import models
from django.core.validators import RegexValidator

cep_validator = RegexValidator(
    regex=r'^\d{5}-?\d{3}$',
    message='Digite um CEP válido no formato 00000-000 ou 00000000.'
)



class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(
        max_length=9,
        validators=[cep_validator],
        help_text='Digite um CEP válido no formato 00000-000 ou 00000000.'
    )

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
    

