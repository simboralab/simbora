from django import forms

from core.models import Endereco

from .models import Eventos


class EventoForm(forms.ModelForm):

    # CAMPOS SEPARADOS (para montar data_inicio, data_termino...)
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "id": "start-date",
        "name": "start_date",
        "required": "required",
        "class": "",
    }))

    start_time = forms.TimeField(widget=forms.TimeInput(attrs={
        "type": "time",
        "id": "start-time",
        "name": "start_time",
        "required": "required",
        "class": "",
    }))

    end_date = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "id": "end-date",
        "name": "end_date",
        "required": "required",
        "class": "",
    }))

    end_time = forms.TimeField(widget=forms.TimeInput(attrs={
        "type": "time",
        "id": "end-time",
        "name": "end_time",
        "required": "required",
        "class": "",
    }))

    meeting_point_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        "type": "date",
        "id": "meeting-point-date",
        "name": "meeting_point_date",
        "class": "",
    }))

    meeting_point_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={
        "type": "time",
        "id": "meeting-point-time",
        "name": "meeting_point_time",
        "class": "",
    }))

    class Meta:
        model = Eventos
        fields = [
            "nome_evento", 
            "categoria", 
            "descricao",
            "tags_input",
            "minimo_participantes",
            "maximo_participantes",
            "ponto_encontro",
            "ponto_endereco",
            "foto",
            "nome_local",
            "foto_url",
            "regras",
            "grupo_whatsapp",
        ]

        widgets = {
            "nome_evento": forms.TextInput(attrs={
                "id": "event-name",
                "placeholder": "Ex: Correr na praia",
            }),
            "categoria": forms.Select(attrs={
                "id": "category",
                "required": "required",
            }),
            "descricao": forms.Textarea(attrs={
                "id": "description",
                "placeholder": "Adicione mais detalhes sobre o seu evento aqui...",
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
                "placeholder": "Ex: Ola de Olinda",
                "required": "required",
            }),

            "ponto_encontro": forms.TextInput(attrs={
                "id": "point-name",
                "placeholder": "Ex: Portão principal do shopping",
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

            "foto_url": forms.HiddenInput(),  # caso use
            "regras": forms.Textarea(attrs={
                "id": "rules",
                "placeholder": "Ex: Ponto de encontro às 19:00…",
            }),
        }

    # JUNTA DATA + HORA → datetime original do model
    def clean(self):
        cleaned = super().clean()

        from datetime import datetime

        sd = cleaned.get("start_date")
        st = cleaned.get("start_time")
        ed = cleaned.get("end_date")
        et = cleaned.get("end_time")

        mpd = cleaned.get("meeting_point_date")
        mpt = cleaned.get("meeting_point_time")

        if sd and st:
            cleaned["data_inicio"] = datetime.combine(sd, st)
        if ed and et:
            cleaned["data_termino"] = datetime.combine(ed, et)
        if mpd and mpt:
            cleaned["data_encontro"] = datetime.combine(mpd, mpt)

        return cleaned

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "rua", "numero", "complemento",
            "bairro", "cidade", "estado", "cep"
        ]
        
        widgets = { 
            "rua": forms.TextInput(attrs={
                "id": "address",
                "placeholder": "Ex: Av. Paulista",
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
            })
        }