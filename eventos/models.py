"""
Modelo de Eventos - Sistema Simbora

 COMO TESTAR:
    1. Django Shell: python manage.py shell
    2. Testar validações: evento.full_clean()
    3. Testar properties: print(evento.vagas_disponiveis)
    4. Script de testes: python manage.py shell < eventos/testes_alunos.py

  CONCEITOS IMPORTANTES:
    - clean(): Validações customizadas (executa em forms/admin)
    - @property: Campos calculados (executam toda vez que acessa)
    - related_name: Nome para acesso reverso (perfil.eventos_organizados)
    - on_delete: O que fazer quando objeto relacionado é deletado
"""

from django.db import models
from perfil.models import Perfil
from core.models import Endereco
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Participacao(models.Model):
    """
    Modelo intermediário para rastrear participação em eventos
    
    Registra o status da participação de cada pessoa em um evento.
    Permite que participantes avaliem o host (organizador) após o evento.
    
    Status possíveis:
        - INSCRITO: Acabou de se inscrever
        - CONFIRMADO: Confirmou que vai participar
        - LISTA_ESPERA: Evento lotou, está na fila
        - CANCELADO: Cancelou a participação
        - PRESENTE: Compareceu ao evento
        - AUSENTE: Não compareceu
    """
    
    STATUS_CHOICES = [
        ('INSCRITO', 'Inscrito'),
        ('CONFIRMADO', 'Confirmado'),
        ('LISTA_ESPERA', 'Lista de Espera'),
        ('CANCELADO', 'Cancelado'),
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
    ]
    
    evento = models.ForeignKey(
        'Eventos',
        on_delete=models.CASCADE,
        related_name='participacoes',
        help_text='Evento ao qual a participação se refere'
    )
    
    participante = models.ForeignKey(
        Perfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='participacoes',
        help_text='Perfil do participante (pode ser nulo se conta foi deletada)'
    )
    

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='INSCRITO',
        help_text='Status atual da participação'
    )
    
    
    data_inscricao = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora da inscrição'
    )
    
    data_cancelamento = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Data e hora do cancelamento'
    )
    
   
    avaliacao_host = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Avaliação do host/organizador (1 a 5 estrelas)'
    )
    
    comentario_host = models.TextField(
        blank=True,
        null=True,
        help_text='Comentário sobre o host/organizador do evento'
    )
    
    class Meta:
        verbose_name = 'Participação'
        verbose_name_plural = 'Participações'
        unique_together = [['evento', 'participante']]
        ordering = ['-data_inscricao']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-data_inscricao']),
        ]
    
    def __str__(self):
        if self.participante:
            participante_nome = self.participante.nome_social or self.participante.usuario.nome_completo
        else:
            participante_nome = "[Usuário Removido]"
        
        return f"{participante_nome} - {self.evento.nome_evento} ({self.get_status_display()})"


class Eventos(models.Model):
    """
    Modelo para gerenciar eventos criados pelos usuários
    
    Campos principais:
        - nome_evento: Nome do evento
        - organizador: Quem criou o evento (pode ser None se perfil deletado)
        - participantes: Lista de participantes (ManyToMany)
        - endereco: Local do evento (opcional para eventos online)
        - data_inicio/data_termino: Datas do evento
        - minimo_participantes: Mínimo para evento acontecer (None = sem mínimo)
        - maximo_participantes: Máximo de pessoas (None = ilimitado)
        - aceita_participantes: Se ainda aceita inscrições
        - status: ATIVO, CANCELADO ou FINALIZADO
    
    Related Names (acesso reverso):
        - perfil.eventos_organizados.all() => eventos que organizou
        - perfil.eventos_participando.all() => eventos que participa
        - endereco.eventos.all() => eventos neste local
    
    Properties:
        TODO: vagas_disponiveis - Calcula vagas restantes
        TODO: esta_lotado - Verifica se lotou ou fechou
        TODO: atingiu_minimo - Verifica se atingiu quórum mínimo
        TODO: status_quorum - Status do quórum ("Confirmado", "Aguardando N")
        TODO: percentual_atingido_minimo - % de progresso até mínimo
        TODO: ja_iniciou - Se evento começou
        TODO: ja_terminou - Se evento terminou
        TODO: percentual_ocupacao - % de vagas ocupadas
        
    Validações implementadas:
        - data_termino > data_inicio
        TODO: minimo_participantes <= maximo_participantes
        TODO: Organizador obrigatório para eventos ativos
        TODO: Localização obrigatória para eventos
        TODO: Eventos ativos não podem ter data no passado
    """

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('CANCELADO', 'Cancelado'),
        ('FINALIZADO', 'Finalizado'),
    ]

    nome_evento = models.CharField(
        max_length=200,
        help_text='Nome do evento'
    )

    organizador = models.ForeignKey(
        Perfil, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_organizados',
        help_text='Perfil do organizador do evento (pode ser nulo se o perfil for deletado)'
    )
    
    participantes = models.ManyToManyField(
        Perfil,
        through='Participacao',
        related_name='eventos_participando',
        blank=True,
        help_text='Perfis dos participantes do evento'
    )
    
    endereco = models.ForeignKey(
        Endereco, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos',
        help_text='Endereço onde o evento acontecerá'
    )
    
    descricao = models.TextField(
        blank=True, 
        null=True,
        help_text='Descrição detalhada do evento'
    )
    
    regras = models.TextField(
        blank=True, 
        null=True,
        help_text='Regras e orientações para os participantes'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ATIVO',
        help_text='Status atual do evento'
    )
    
    data_inicio = models.DateTimeField(
        help_text='Data e hora de início do evento'
    )
    
    data_termino = models.DateTimeField(
        help_text='Data e hora de término do evento'
    )
    
    data_encontro = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data e hora do ponto de encontro (se diferente do início)'
    )
    

    local_encontro = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text='Descrição do local de encontro (ponto de referência)'
    )
    
    grupo_whatsapp = models.URLField(
        max_length=500,
        blank=True, 
        null=True,
        help_text='Link do grupo do WhatsApp para o evento'
    )
    
    foto = models.ImageField(
        upload_to='images/eventos/',
        blank=True,
        null=True,
        help_text='Foto principal do evento'
    )
    
    foto_url = models.URLField(
        blank=True, 
        null=True,
        help_text='URL de uma imagem hospedada externamente'
    )
    
    minimo_participantes = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Número mínimo de participantes para o evento acontecer'
    )
    
    maximo_participantes = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Número máximo de participantes (deixe em branco para ilimitado)'
    )
    
    aceita_participantes = models.BooleanField(
        default=True,
        help_text='Se o evento ainda está aceitando novos participantes'
    )
    
    CATEGORIA_CHOICES = [
        ('ESPORTE', 'Esporte'),
        ('LAZER', 'Lazer'),
        ('CULTURA', 'Cultura'),
        ('TECNOLOGIA', 'Tecnologia'),
        ('EDUCACAO', 'Educação'),
    ]
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        blank=True,
        null=True,
        help_text='Categoria do evento'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Data de criação do evento'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Data da última atualização'
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['-data_inicio']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.nome_evento} - {self.data_inicio.strftime('%d/%m/%Y')}"
    
    def clean(self):
        """
        Validações customizadas do modelo
        
        Este método é executado automaticamente em Forms e no Django Admin.
        Para usar em código Python, chame: objeto.full_clean()
        """
        super().clean() 
        
        # Valida que data_termino é posterior a data_inicio
        if self.data_inicio and self.data_termino:
            if self.data_termino <= self.data_inicio:
                raise ValidationError({
                    'data_termino': 'A data de término deve ser posterior à data de início.'
                })
        
        # TODO: Validar que minimo_participantes <= maximo_participantes

        # TODO: Validar que data_encontro (se informada) não é posterior ao início
        
        # TODO: Validar que eventos ativos não podem ser criados no passado

        # TODO: Eventos ativos/concluidos devem ter organizador
        # Justificativa: null=True permite histórico, mas evento novo precisa de organizador
        
        # TODO: Eventos devem ter endereço OU local_encontro
        # Justificativa: Participantes precisam saber onde ir

   
    
    @property
    def vagas_disponiveis(self):
        """
        Retorna o número de vagas disponíveis
        
        Considera:
        - maximo_participantes: Máximo de pessoas permitidas
        - aceita_participantes: Se ainda está aceitando inscrições
        
        Retorna:
        - None: Vagas ilimitadas E aceitando participantes
        - 0: Lotado OU não aceita mais participantes
        - N: Número de vagas restantes
        """
        # TODO: Implementar
        pass
    
    @property
    def esta_lotado(self):
        """
        Verifica se o evento está lotado ou fechado para inscrições
        
        Retorna True se:
        - Atingiu o máximo de participantes OU
        - Não aceita mais novos participantes
        """
        # TODO: Implementar
        pass
    
    @property
    def atingiu_minimo(self):
        """
        Verifica se atingiu o mínimo de participantes
        
        Retorna:
        - True: Atingiu o mínimo (evento confirmado)
        - False: Não atingiu (evento em risco de cancelamento)
        - None: Não tem mínimo definido (sempre confirmado)
        """
        # TODO: Implementar
        pass
    
    @property
    def status_quorum(self):
        """
        Retorna status do quórum mínimo
        
        Retorna:
        - "Confirmado": Atingiu mínimo
        - "Aguardando N pessoas": Faltam N para atingir mínimo
        - "Sem mínimo": Não tem mínimo definido
        """
        # TODO: Implementar
        pass
    
    @property
    def percentual_atingido_minimo(self):
        """
        Retorna percentual de progresso até o mínimo
        Útil para barras de progresso
        
        Retorna: 0-100 (ou 100 se não tem mínimo ou já atingiu)
        """
        # TODO: Implementar
        pass
    
    @property
    def ja_iniciou(self):
        """
        Verifica se o evento já iniciou
        
        # TODO:
        Retorna: True se evento já começou, False caso contrário
        """
        # TODO: Implementar
        pass
    
    @property
    def ja_terminou(self):
        """
        Verifica se o evento já terminou
        Retorna: True se evento já terminou, False caso contrário
        
        Uso: Mostrar badge "Encerrado" em eventos passados
        """
        # TODO: Implementar
        pass
    
    
    @property
    def percentual_ocupacao(self):
        """
            Retorna o percentual de vagas ocupadas (0-100)
            Útil para barras de progresso e alertas
        """
        #TODO: Implementar
        pass
    
