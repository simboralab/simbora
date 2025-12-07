from django import forms
from django.utils import timezone
from .models import Eventos

class EventoForm(forms.ModelForm):

    class Meta:
        model = Eventos
        fields = [
            'nome_evento',
            'descricao',
            'regras',
            'status',
            'data_inicio',
            'data_termino',
            'data_encontro',
            'local_encontro',
            'endereco',
            'grupo_whatsapp',
            'foto',
            'foto_url',
            'minimo_participantes',
            'maximo_participantes',
            'aceita_participantes',
        ]

        widgets = {
            'nome_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Pelada de sábado no parque'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o evento com detalhes'
            }),
            'regras': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Regras, critérios, observações...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_inicio': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'data_termino': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'data_encontro': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'local_encontro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ponto de encontro, referência...'
            }),
            'endereco': forms.Select(attrs={
                'class': 'form-control'
            }),
            'grupo_whatsapp': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link do grupo de WhatsApp'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'foto_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL de imagem externa'
            }),
            'minimo_participantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'maximo_participantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'aceita_participantes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    # --------------------------------------------------------------------
    # CLEAN — validações adicionais
    # --------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean()

        data_inicio = cleaned_data.get('data_inicio')
        data_termino = cleaned_data.get('data_termino')
        data_encontro = cleaned_data.get('data_encontro')
        status = cleaned_data.get('status')

        minimo = cleaned_data.get('minimo_participantes')
        maximo = cleaned_data.get('maximo_participantes')

        endereco = cleaned_data.get('endereco')
        local_encontro = cleaned_data.get('local_encontro')

        foto = cleaned_data.get('foto')
        foto_url = cleaned_data.get('foto_url')

        # ------------------------------------------------
        # 1) Foto: não pode enviar arquivo e URL juntos
        # ------------------------------------------------
        if foto and foto_url:
            self.add_error('foto_url', 'Escolha apenas uma opção: foto OU foto por URL.')

        # ------------------------------------------------
        # 2) Validação mínima/máxima no formulário também
        # ------------------------------------------------
        if minimo and maximo:
            if minimo > maximo:
                self.add_error('minimo_participantes', 
                    'O mínimo de participantes não pode ser maior que o máximo.')

        # ------------------------------------------------
        # 3) Endereço ou local de encontro obrigatório
        # ------------------------------------------------
        if not endereco and not local_encontro:
            raise forms.ValidationError(
                'Informe um endereço OU um local de encontro.'
            )

        # ------------------------------------------------
        # 4) Datas: início < término
        # ------------------------------------------------
        if data_inicio and data_termino:
            if data_termino <= data_inicio:
                self.add_error('data_termino',
                    'A data de término deve ser posterior à data de início.')

        # ------------------------------------------------
        # 5) Data do encontro < início
        # ------------------------------------------------
        if data_encontro and data_inicio:
            if data_encontro > data_inicio:
                self.add_error('data_encontro',
                    'A data do encontro deve ser antes do início do evento.')

        # ------------------------------------------------
        # 6) Eventos ATIVOS não podem começar no passado
        # ------------------------------------------------
        if status == 'ATIVO' and data_inicio:
            if data_inicio < timezone.now():
                self.add_error('data_inicio',
                    'Eventos ativos não podem ter início no passado.')

        return cleaned_data
