from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from perfil.models import Perfil
from core.models import Endereco
from eventos.models import Eventos, Participacao


class Command(BaseCommand):
    help = 'Popula o banco de dados com exemplos de eventos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando cadastro de eventos de exemplo...'))
        
        try:
            with transaction.atomic():
                # Verificar se existem perfis
                if Perfil.objects.count() == 0:
                    self.stdout.write(self.style.ERROR('❌ Não há perfis cadastrados!'))
                    self.stdout.write('Execute primeiro: python manage.py popular_dados')
                    return
                
                # Verificar se existem endereços
                if Endereco.objects.count() == 0:
                    self.stdout.write(self.style.ERROR('❌ Não há endereços cadastrados!'))
                    self.stdout.write('Execute primeiro: python manage.py popular_dados')
                    return
                
                # Pegar alguns perfis e endereços
                perfis = list(Perfil.objects.all()[:5])
                enderecos = list(Endereco.objects.all()[:5])
                
                self.stdout.write(f'\nEncontrados {len(perfis)} perfis e {len(enderecos)} endereços')
                
                # ========== CRIAR EVENTOS ==========
                self.stdout.write('\n--- Cadastrando Eventos ---')
                
                agora = timezone.now()
                
                # Evento 1 - Trilha no Parque
                evento1 = Eventos.objects.create(
                    nome_evento='Trilha no Parque Ibirapuera',
                    descricao='Vamos fazer uma trilha leve no Parque Ibirapuera. Ideal para iniciantes! Traremos lanche compartilhado ao final.',
                    organizador=perfis[0],
                    endereco=enderecos[0],
                    data_inicio=agora + timedelta(days=7, hours=9),
                    data_termino=agora + timedelta(days=7, hours=12),
                    data_encontro=agora + timedelta(days=7, hours=8, minutes=30),
                    local_encontro='Portão 3 do Parque Ibirapuera',
                    status='ATIVO',
                    minimo_participantes=5,
                    maximo_participantes=15,
                    aceita_participantes=True,
                    regras='- Trazer água\n- Usar roupas confortáveis\n- Respeitar o ritmo do grupo\n- Não deixar lixo na trilha',
                    grupo_whatsapp='https://chat.whatsapp.com/exemplo123'
                )
                # Adicionar participantes
                Participacao.objects.create(evento=evento1, participante=perfis[1], status='CONFIRMADO')
                Participacao.objects.create(evento=evento1, participante=perfis[2], status='INSCRITO')
                
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento1.nome_evento}'))
                self.stdout.write(f'  Organizador: {evento1.organizador.nome_social or evento1.organizador.usuario.nome_completo}')
                self.stdout.write(f'  Participantes: {evento1.participacoes.count()}')
                self.stdout.write(f'  Vagas: {evento1.vagas_disponiveis}/{evento1.maximo_participantes}')
                
                # Evento 2 - Cinema ao Ar Livre
                evento2 = Eventos.objects.create(
                    nome_evento='Cinema ao Ar Livre - Filmes Clássicos',
                    descricao='Sessão de cinema ao ar livre com filmes clássicos brasileiros. Traga sua cadeira ou canga!',
                    organizador=perfis[1],
                    endereco=enderecos[1],
                    data_inicio=agora + timedelta(days=5, hours=19),
                    data_termino=agora + timedelta(days=5, hours=22),
                    local_encontro='Entrada principal do Centro Cultural',
                    status='ATIVO',
                    minimo_participantes=10,
                    maximo_participantes=30,
                    aceita_participantes=True,
                    regras='- Evento gratuito\n- Trazer cadeira ou canga\n- Silêncio durante o filme\n- Uso de fones de ouvido para quem quiser dublagem',
                )
                # Adicionar participantes
                Participacao.objects.create(evento=evento2, participante=perfis[0], status='CONFIRMADO')
                Participacao.objects.create(evento=evento2, participante=perfis[2], status='CONFIRMADO')
                Participacao.objects.create(evento=evento2, participante=perfis[3], status='INSCRITO')
                
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento2.nome_evento}'))
                self.stdout.write(f'  Organizador: {evento2.organizador.nome_social or evento2.organizador.usuario.nome_completo}')
                self.stdout.write(f'  Participantes: {evento2.participacoes.count()}')
                
                # Evento 3 - Piquenique Literário
                evento3 = Eventos.objects.create(
                    nome_evento='Piquenique Literário - Clube do Livro',
                    descricao='Encontro mensal do clube do livro com piquenique. Mês atual: discutiremos "Grande Sertão: Veredas".',
                    organizador=perfis[2],
                    endereco=enderecos[2],
                    data_inicio=agora + timedelta(days=14, hours=10),
                    data_termino=agora + timedelta(days=14, hours=14),
                    local_encontro='Próximo ao lago do parque',
                    status='ATIVO',
                    minimo_participantes=4,
                    maximo_participantes=12,
                    aceita_participantes=True,
                    regras='- Ter lido o livro do mês\n- Trazer algo para compartilhar no piquenique\n- Respeitar opiniões diferentes\n- Manter celular no silencioso',
                    grupo_whatsapp='https://chat.whatsapp.com/livros456'
                )
                # Adicionar participantes
                Participacao.objects.create(evento=evento3, participante=perfis[0], status='PRESENTE')  # Já participou
                Participacao.objects.create(evento=evento3, participante=perfis[1], status='CONFIRMADO')
                Participacao.objects.create(evento=evento3, participante=perfis[4], status='INSCRITO')
                
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento3.nome_evento}'))
                
                # Evento 4 - Pedalada Urbana (RASCUNHO)
                evento4 = Eventos.objects.create(
                    nome_evento='Pedalada Urbana - Ciclovia Rio Pinheiros',
                    descricao='Pedal leve pela ciclovia do Rio Pinheiros. Ideal para quem está começando a pedalar.',
                    organizador=perfis[3],
                    endereco=enderecos[3],
                    data_inicio=agora + timedelta(days=21, hours=7),
                    data_termino=agora + timedelta(days=21, hours=10),
                    local_encontro='Estação de bike próxima à ponte',
                    status='ATIVO',
                    minimo_participantes=8,
                    maximo_participantes=20,
                    aceita_participantes=True,
                    regras='- Bike em bom estado\n- Uso obrigatório de capacete\n- Respeitar sinalização'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento4.nome_evento}'))
                
                # Evento 5 - Aula de Yoga (evento lotado)
                evento5 = Eventos.objects.create(
                    nome_evento='Yoga ao Nascer do Sol',
                    descricao='Aula de yoga gratuita ao ar livre. Para todos os níveis, do iniciante ao avançado.',
                    organizador=perfis[4],
                    endereco=enderecos[4],
                    data_inicio=agora + timedelta(days=3, hours=6),
                    data_termino=agora + timedelta(days=3, hours=7, minutes=30),
                    local_encontro='Gramado central',
                    status='ATIVO',
                    minimo_participantes=3,
                    maximo_participantes=5,
                    aceita_participantes=True,
                    regras='- Trazer tapete de yoga\n- Chegar 10min antes\n- Usar roupas confortáveis\n- Silêncio absoluto',
                    grupo_whatsapp='https://chat.whatsapp.com/yoga789'
                )
                # Adicionar participantes até lotar
                Participacao.objects.create(evento=evento5, participante=perfis[0], status='CONFIRMADO')
                Participacao.objects.create(evento=evento5, participante=perfis[1], status='CONFIRMADO')
                Participacao.objects.create(evento=evento5, participante=perfis[2], status='CONFIRMADO')
                Participacao.objects.create(evento=evento5, participante=perfis[3], status='INSCRITO')
                
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento5.nome_evento}'))
                self.stdout.write(self.style.WARNING(f'  ⚠️  LOTADO! ({evento5.participacoes.count()}/{evento5.maximo_participantes})'))
                
                # Evento 6 - Sarau de Poesia (CANCELADO - não atingiu mínimo)
                evento6 = Eventos.objects.create(
                    nome_evento='Sarau de Poesia - Vozes da Cidade',
                    descricao='Sarau aberto para declamação de poesias autorais e de poetas consagrados.',
                    organizador=perfis[0],
                    endereco=enderecos[0],
                    data_inicio=agora + timedelta(days=2, hours=19),
                    data_termino=agora + timedelta(days=2, hours=22),
                    local_encontro='Salão principal',
                    status='CANCELADO',
                    minimo_participantes=10,
                    maximo_participantes=30,
                    aceita_participantes=False,
                )
                # Evento cancelado - sem participantes suficientes
                self.stdout.write(self.style.WARNING(f'✓ Evento criado: {evento6.nome_evento} (CANCELADO - não atingiu mínimo)'))
                self.stdout.write(f'  Nenhuma participação registrada')
                
                # Evento 7 - Workshop de Fotografia (evento sem limite)
                evento7 = Eventos.objects.create(
                    nome_evento='Workshop de Fotografia - Luz Natural',
                    descricao='Aprenda técnicas de fotografia usando apenas luz natural. Traga sua câmera ou celular!',
                    organizador=perfis[1],
                    endereco=enderecos[1],
                    data_inicio=agora + timedelta(days=10, hours=14),
                    data_termino=agora + timedelta(days=10, hours=17),
                    local_encontro='Praça da fonte',
                    status='ATIVO',
                    minimo_participantes=5,
                    maximo_participantes=None,  # Ilimitado
                    aceita_participantes=True,
                    regras='- Trazer câmera ou celular\n- Bateria carregada\n- Respeitar os modelos',
                    grupo_whatsapp='https://chat.whatsapp.com/foto000'
                )
                # Adicionar participantes
                Participacao.objects.create(evento=evento7, participante=perfis[2], status='CONFIRMADO')
                Participacao.objects.create(evento=evento7, participante=perfis[3], status='CONFIRMADO')
                Participacao.objects.create(evento=evento7, participante=perfis[4], status='INSCRITO')
                
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento7.nome_evento} (Vagas ilimitadas)'))
                
                # Evento 8 - Evento Finalizado (com avaliações)
                evento8 = Eventos.objects.create(
                    nome_evento='Caminhada Noturna - Centro Histórico',
                    descricao='Caminhada guiada pelo centro histórico da cidade. Evento já realizado.',
                    organizador=perfis[0],
                    endereco=enderecos[0],
                    data_inicio=agora - timedelta(days=5, hours=19),  # Evento no passado
                    data_termino=agora - timedelta(days=5, hours=21),
                    local_encontro='Praça Central',
                    status='FINALIZADO',
                    minimo_participantes=6,
                    maximo_participantes=15,
                    aceita_participantes=False,
                    regras='- Calçado confortável\n- Trazer garrafa de água'
                )
                
                # Participantes com diferentes status e avaliações
                Participacao.objects.create(
                    evento=evento8, 
                    participante=perfis[1], 
                    status='PRESENTE',
                    avaliacao_host=5,
                    comentario_host='Excelente organizador! Evento muito bem planejado.'
                )
                Participacao.objects.create(
                    evento=evento8, 
                    participante=perfis[2], 
                    status='PRESENTE',
                    avaliacao_host=4,
                    comentario_host='Muito bom, organizador atencioso.'
                )
                Participacao.objects.create(
                    evento=evento8, 
                    participante=perfis[3], 
                    status='AUSENTE'  # Não compareceu
                )
                Participacao.objects.create(
                    evento=evento8, 
                    participante=perfis[4], 
                    status='CANCELADO',
                    data_cancelamento=agora - timedelta(days=6)
                )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Evento criado: {evento8.nome_evento} (FINALIZADO)'))
                self.stdout.write(f'  Participações: {evento8.participacoes.count()}')
                self.stdout.write(f'  Presentes: {evento8.participacoes.filter(status="PRESENTE").count()}')
                self.stdout.write(f'  Ausentes: {evento8.participacoes.filter(status="AUSENTE").count()}')
                self.stdout.write(f'  Cancelados: {evento8.participacoes.filter(status="CANCELADO").count()}')
                
                # Adicionar algumas avaliações ao evento3 também (evento em andamento)
                participacao_evento3 = evento3.participacoes.filter(participante=perfis[0]).first()
                if participacao_evento3:
                    participacao_evento3.status = 'PRESENTE'
                    participacao_evento3.avaliacao_host = 5
                    participacao_evento3.comentario_host = 'Organizador super preparado!'
                    participacao_evento3.save()
                
                # ========== RESUMO ==========
                self.stdout.write('\n' + '='*60)
                self.stdout.write(self.style.SUCCESS('RESUMO DOS EVENTOS:'))
                self.stdout.write(f'Total de eventos cadastrados: {Eventos.objects.count()}')
                self.stdout.write(f'  - Ativos: {Eventos.objects.filter(status="ATIVO").count()}')
                self.stdout.write(f'  - Cancelados: {Eventos.objects.filter(status="CANCELADO").count()}')
                self.stdout.write(f'  - Finalizados: {Eventos.objects.filter(status="FINALIZADO").count()}')
                
                self.stdout.write(f'\nTotal de participações: {Participacao.objects.count()}')
                self.stdout.write(f'  - Inscritos: {Participacao.objects.filter(status="INSCRITO").count()}')
                self.stdout.write(f'  - Confirmados: {Participacao.objects.filter(status="CONFIRMADO").count()}')
                self.stdout.write(f'  - Presentes: {Participacao.objects.filter(status="PRESENTE").count()}')
                self.stdout.write(f'  - Ausentes: {Participacao.objects.filter(status="AUSENTE").count()}')
                self.stdout.write(f'  - Cancelados: {Participacao.objects.filter(status="CANCELADO").count()}')
                
                avaliacoes = Participacao.objects.filter(avaliacao_host__isnull=False)
                if avaliacoes.exists():
                    from django.db.models import Avg
                    media = avaliacoes.aggregate(Avg('avaliacao_host'))['avaliacao_host__avg']
                    self.stdout.write(f'\nAvaliações de hosts: {avaliacoes.count()} avaliações')
                    self.stdout.write(f'  Média geral: {media:.2f} ⭐')
                
                self.stdout.write('='*60)
                
                self.stdout.write(self.style.SUCCESS('\n✅ Eventos e participações cadastrados com sucesso!'))
                self.stdout.write('\nAcesse o admin em:')
                self.stdout.write('  Eventos: http://127.0.0.1:8000/admin/eventos/eventos/')
                self.stdout.write('  Participações: http://127.0.0.1:8000/admin/eventos/participacao/')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Erro ao cadastrar eventos: {str(e)}'))
            import traceback
            traceback.print_exc()
            raise

