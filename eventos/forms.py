from django import forms
from django.core.exceptions import ValidationError
from core.models import Endereco
from .models import Eventos


class EventoForm(forms.ModelForm):

    # CAMPOS SEPARADOS (para montar data_inicio, data_termino...)
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "id": "start-date",
        "required": "required",
    }))

    horario_inicial = forms.TimeField(widget=forms.TimeInput(attrs={
        "type": "time",
        "id": "start-time",
        "required": "required",
    }))

    data_final = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "id": "end-date",
        "required": "required",
        "class": "",
    }))

    horario_final = forms.TimeField(widget=forms.TimeInput(attrs={
        "type": "time",
        "id": "end-time",
        "required": "required",
        "class": "",
    }))

    data_encontro = forms.DateField(required=False, widget=forms.DateInput(attrs={
        "type": "date",
        "id": "meeting-point-date",
        "class": "",
    }))

    horario_encontro = forms.TimeField(required=False, widget=forms.TimeInput(attrs={
        "type": "time",
        "id": "meeting-point-time",
        "class": "",
    }))

    CATEGORY_CHOICES = [
        ("", "Selecione uma categoria"),
        ("TEC", "Tecnologia"),
        ("EDU", "Educação"),
        ("ESP", "Esporte"),
        ("CUL", "Cultura"),
        ("OUT", "Outros"),
    ]

    categoria = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            "id": "category",
        })
    )

    class Meta:
        model = Eventos
        fields = "__all__"
        exclude = ['organizador', 'status','data_inicio', 'data_termino']

        widgets = {
            "nome_evento": forms.TextInput(attrs={
                "id": "event-name",
                "placeholder": "Ex: Correr na praia",
            }),

            "descricao": forms.Textarea(attrs={
                "id": "description",
                "placeholder": "Adicione detalhes sobre o evento...",
            }),

            "grupo_whatsapp": forms.URLInput(attrs={
                "id": "whatsapp-link",
                "placeholder": "https://chat.whatsapp.com/...",
                "pattern": "https://chat\.whatsapp\.com/.+",
                "required": "required",
            }),

            "tags_input": forms.TextInput(attrs={
                "id": "tags-input",
                "placeholder": "Digite uma tag e pressione Enter",
                "autocomplete": "off",
            }),

            "nome_local": forms.TextInput(attrs={
                "id": "location-name",
                "placeholder": "Ex: Praça Boa Viagem",
                "required": "required",
            }),

            "local_encontro": forms.TextInput(attrs={
                "id": "point-name",
                "placeholder": "Portão principal do shopping",
            }),

            "ponto_endereco": forms.TextInput(attrs={
                "id": "meeting-point-address",
                "placeholder": "Ex: Av. Boa Viagem, 1000 - Boa Viagem",
            }),

            "ponto_descricao": forms.Textarea(attrs={
                "id": "meeting-point-description",
                "placeholder": "Ex: Vou estar com uma camisa amarela...",
            }),

            "minimo_participantes": forms.NumberInput(attrs={
                "id": "min-people",
                "placeholder": "2",
                "min": "1",
            }),

            "maximo_participantes": forms.NumberInput(attrs={
                "id": "max-people",
                "placeholder": "10",
                "min": "1",
            }),

            "foto": forms.FileInput(attrs={
                "id": "cover-image",
                "class": "file-input",
                "accept": "image/jpeg,image/jpg,image/png",
            }),

            "foto_url": forms.HiddenInput(),

            "regras": forms.Textarea(attrs={
                "id": "rules",
                "placeholder": "Ex: Ponto de encontro às 19:00...",
            }),
        }

    # MONTA data_inicio, data_termino e data_encontro
    def clean(self):
        cleaned = super().clean()

        from datetime import datetime
        from django.utils import timezone

        sd = cleaned.get("data_inicial")
        st = cleaned.get("horario_inicial")
        ed = cleaned.get("data_final")
        et = cleaned.get("horario_final")

        mpd = cleaned.get("data_encontro")
        mpt = cleaned.get("horario_encontro")

        # monta datetimes timezone-aware
        if sd and st:
            cleaned["data_inicio"] = timezone.make_aware(datetime.combine(sd, st))

        if ed and et:
            cleaned["data_termino"] = timezone.make_aware(datetime.combine(ed, et))

        if mpd and mpt:
            cleaned["data_encontro"] = timezone.make_aware(datetime.combine(mpd, mpt))

        return cleaned

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')

        # Se usuário deixar a primeira opção "", voltar None
        if categoria == '':
            return None
        return categoria


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "rua", "numero", "complemento",
            "bairro", "cidade", "estado", "cep"
        ]

        widgets = {
            "rua": forms.TextInput(attrs={
                "id": "street",
                "placeholder": "Ex: Orla. Olinda",
                "required": "required",
            }),
            "numero": forms.NumberInput(attrs={
                "id": "number",
                "placeholder": "1000",
            }),
            "cep": forms.TextInput(attrs={
                "id": "cep",
                "placeholder": "00000-000",
                "pattern": r"\d{5}-\d{3}",
            }),
            "bairro": forms.TextInput(attrs={
                "id": "neighborhood",
                "placeholder": "Bela Vista",
            }),
            "cidade": forms.TextInput(attrs={
                "id": "city",
                "placeholder": "São Paulo",
            }),
            "estado": forms.TextInput(attrs={
                "id": "state",
                "placeholder": "PE",
            }),
            "complemento": forms.TextInput(attrs={
                "id": "complement",
                "placeholder": "Ap 102, Bloco B",
            })
        }
