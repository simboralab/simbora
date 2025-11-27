from django.db import models
from perfil.models import Perfil
from core.models import Endereco
from django.core.validators import MinValueValidator 
from django.utils import timezone


class Eventos(models.Model):
    organizador = models.ForeignKey(
        Perfil, on_delete=models.CASCADE, related_name='organizador'
    )
    participantes = models.ManyToManyField (
        Perfil, related_name='participantes'
    )
    endereco = models.ForeignKey (
        Endereco, 
        on_delete=models.CASCADE
    )
    nome_evento = models.CharField (
        max_length=20, 
        blank=True, 
        null=True
    )
    descricao = models.CharField (
        max_length=500, 
        blank=True, 
        null=True
    )
    grupo_whatsapp = models.CharField (
        max_length=250, 
        blank=True, 
        null=True
    )
    data_inicio = models.DateTimeField (
        auto_now=True, 
        validators=[MinValueValidator(timezone.now())]
    )
    data_termino = models.DateTimeField (
        auto_now=True, 
        validators=[MinValueValidator(timezone.now())]
    )
    local_encontro = models.CharField (
        max_length=500, 
        blank=True, 
        null=True
    )
    data_encontro = models.DateTimeField (
        auto_now=True, 
        validators=[MinValueValidator(timezone.now())]
    )
    foto_url = models.URLField (
        blank=True, 
        null=True
    )
    foto = models.ImageField(
        upload_to='images/eventos'
    )
    regras = models.CharField (
        max_length=500, 
        blank=True, 
        null=True
    )