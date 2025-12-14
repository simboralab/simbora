# forms.py

from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Usuario, Perfil

GENERO_CHOICES = [
    ('', 'Selecione seu gênero'), 
    ('HOMEM_CIS', 'Homem cis'),
    ('MULHER_CIS', 'Mulher cis'),
    ('HOMEM_TRANS', 'Homem Trans'),
    ('MULHER_TRANS', 'Mulher Trans'),
    ('NAO_BINARIO', 'Não-binário'),
    ('AGENERO', 'Agênero'),
    ('GENERO_FLUIDO', 'Gênero fluido'),
    ('OUTRO', 'Outro'),
    ('NAO_INFORMAR', 'Prefiro não informar'),
]

class CadastroUsuarioBaseForm(UserCreationForm):
    class Meta:
        model = Usuario
   
        fields = ('email', 'first_name', 'last_name','password1', 'password2') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajustando rótulos dos campos do modelo
        # Mapeamento dos campos do UserCreationForm para os IDs do seu HTML
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs.update({'id': 'id_email_cadastro', 'placeholder': 'Digite seu e-mail'})
        
        self.fields['first_name'].label = 'Primeiro nome'
        self.fields['first_name'].widget.attrs.update({'id': 'id_nome', 'placeholder': 'Digite seu nome'})
        
        self.fields['last_name'].label = 'Último nome'
        self.fields['last_name'].widget.attrs.update({'id': 'id_sobrenome', 'placeholder': 'Digite seu sobrenome'})

        self.fields['password1'].label = 'Senha'
        self.fields['password1'].widget.attrs.update({'id': 'id_senha_cadastro', 'placeholder': 'Digite sua senha'})

        self.fields['password2'].label = 'Confirmação de senha'
        self.fields['password2'].widget.attrs.update({'id': 'id_confirmar_senha', 'placeholder': 'Confirme sua senha'})
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
    
        # Garante que a verificação só ocorra se o email não estiver vazio
        if not email:
            raise forms.ValidationError("O campo Email é obrigatório.")
        
        # Verifica se já existe um usuário com este e-mail
        # Usa o mesmo modelo definido no 'Meta'
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado. Tente fazer login ou use outro e-mail."
            )

        return email
      

## Formulário Completo: Adicionando Data de Nascimento
class CadastroCompletoForm(CadastroUsuarioBaseForm):

    data_nascimento = forms.DateField(
        label=_("Data de Nascimento: "),
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/aaaa'}),
        error_messages={'required': 'A data de nascimento é obrigatória.'}
    )

    genero = forms.ChoiceField(
        label=_("Gênero: "),
        choices=GENERO_CHOICES,
        required=True, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_genero(self):
        genero = self.cleaned_data.get('genero')
        
        if genero == '':
            return None 
            
        valid_values = [v[0] for v in GENERO_CHOICES if v[0] != '']
        if genero and genero not in valid_values:
            raise ValidationError("Seleção de gênero inválida.")
            
        return genero

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        
        
        if not data_nascimento:
             return data_nascimento

        hoje = date.today()

        if data_nascimento > hoje:
            raise ValidationError("Data de nascimento inválida (não pode ser futura).")

    
        idade = hoje.year - data_nascimento.year
        if hoje.month < data_nascimento.month or \
           (hoje.month == data_nascimento.month and hoje.day < data_nascimento.day):
            idade -= 1
        
        if idade < 18:
            raise ValidationError("Usuário deve ter pelo menos 18 anos para se cadastrar.")
            
        return data_nascimento
    



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Renomeando o label do campo 'username' para 'Email'
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'placeholder': 'Digite seu e-mail', 'id': 'id_email_login'})
        self.fields['password'].label = 'Senha'
        self.fields['password'].widget.attrs.update({'placeholder': 'Digite sua senha', 'id': 'id_senha_login'})



class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'nome_social',
            'descricao',
            'genero',
            'is_pcd',
            'neurodiversidade',
            'foto_perfil',
        ]

        widgets = {
            'nome_social': forms.TextInput(attrs={'placeholder': 'Informe seu nome social'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Fale mais sobre você...'}),
            'genero': forms.Select(),
        }