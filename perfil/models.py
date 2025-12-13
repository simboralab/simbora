import uuid
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from encrypted_model_fields.fields import EncryptedCharField

cpf_validator = RegexValidator(
    regex=r'^(\d{3}\.?\d{3}\.?\d{3}-?\d{2})$',
    message='Digite um CPF válido (com ou sem pontuação).'
)

class CustomUserManager(UserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve informar um email.")

        email = self.normalize_email(email)

        extra_fields.setdefault('username', email)

        return super().create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', email)

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    
    username = models.CharField(
        max_length=150,
        unique=False,  # <--- REMOVE a restrição UNIQUE
        null=True,     # <--- Permite ser None (nulo) no DB
        blank=True     # <--- Permite ser None/vazio em formulários
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.nome_completo or self.email
    
    @property
    def nome_completo(self): #retorna o nome completo a partir do first_name e last_name que já são nativos do django
        return f"{self.first_name} {self.last_name}".strip()
    
        
class Perfil(models.Model):
    nome_social = models.CharField(max_length=100, blank=True, null=True)

    cpf = EncryptedCharField( 
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        validators=[cpf_validator],
        help_text='Digite um CPF válido (com ou sem pontuação).'
    )

    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True) 

    imagem_url = models.URLField(blank=True, null=True) # PEGA IMAGEM HOSPEDADA NA NET

    descricao = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    is_pcd = models.BooleanField(
        default=False
    )

    neurodiversidade = models.BooleanField(
        default=False
    )

    genero = models.CharField(
        max_length=30,
        choices=[
                ('HOMEM_CIS', 'Homem cis'),
                ('MULHER_CIS', 'Mulher cis'),
                ('HOMEM_TRANS', 'Homem Trans'),
                ('MULHER_TRANS', 'Mulher Trans'),
                ('NAO_BINARIO', 'Não-binário'),
                ('AGENERO', 'Agênero'),
                ('GENERO_FLUIDO', 'Gênero fluido'),
                ('OUTRO', 'Outro'),
                ('NAO_INFORMAR', 'Prefiro não informar'),
            ],
            blank=True,
            null=True
    )

    endereco = models.ForeignKey(
        'core.Endereco',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfis'
    )

    usuario = models.OneToOneField(
        'Usuario',
        on_delete=models.SET_NULL, #Pode trocar pra CASCADE se quiser deletar o perfil quando deletar o usuario
        null=True,
        blank=True,
        related_name='perfil'
    )

    data_nascimento = models.DateField()

    def clean(self):
        super().clean()
        hoje = date.today()

        # Se data_nascimento estiver vazia, não valida nada ainda
        if not self.data_nascimento:
            return

        if self.data_nascimento > hoje:
            raise ValidationError("Data de nascimento inválida.")

        idade_dias = (hoje - self.data_nascimento).days
        if idade_dias < 18 * 365:  # idade mínima
            raise ValidationError("Usuário deve ter pelo menos 18 anos.")


    @property
    def idade(self):
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day): #se ainda n fez aniversario este ano, corrige com -1
            idade -= 1
        return idade
    
    @property
    def nome_completo(self):
        """Retorna o nome completo do perfil: nome_social ou usuario.nome_completo"""
        if self.nome_social:
            return self.nome_social
        elif self.usuario:
            return self.usuario.nome_completo or self.usuario.email
        return f"Perfil #{self.id}"
    
    def __str__(self):
        """Retorna uma representação legível do perfil"""
        return self.nome_completo

