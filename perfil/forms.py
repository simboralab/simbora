# forms.py

from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Usuario


class CadastroUsuarioBaseForm(UserCreationForm):



    class Meta:
        model = Usuario
   
        fields = ('email', 'first_name', 'last_name') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajustando rótulos dos campos do modelo
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'Primeiro nome'
        self.fields['last_name'].label = 'Último nome'
        
      

## Formulário Completo: Adicionando Data de Nascimento
class CadastroCompletoForm(CadastroUsuarioBaseForm):

    data_nascimento = forms.DateField(
        label=_("Data de Nascimento: "),
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/aaaa'}),
        error_messages={'required': 'A data de nascimento é obrigatória.'}
    )

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