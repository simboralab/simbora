from django.core.management.base import BaseCommand
from django.db import transaction
from perfil.models import Perfil, Usuario
from core.models import Endereco
from datetime import date


class Command(BaseCommand):
    help = 'Popula o banco de dados com exemplos de endereços e perfis'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando cadastro de dados de exemplo...'))
        
        try:
            with transaction.atomic():
                # Limpar dados anteriores (opcional - comente se não quiser limpar)
                # Perfil.objects.all().delete()
                # Endereco.objects.all().delete()
                # Usuario.objects.filter(is_superuser=False).delete()
                
                # ========== CADASTRAR ENDEREÇOS ==========
                self.stdout.write('\n--- Cadastrando Endereços ---')
                
                endereco1 = Endereco.objects.create(
                    rua='Avenida Paulista',
                    numero='1000',
                    bairro='Bela Vista',
                    cidade='São Paulo',
                    estado='SP',
                    cep='01310-100'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Endereço 1 criado: {endereco1}'))
                
                endereco2 = Endereco.objects.create(
                    rua='Rua das Flores',
                    numero='123',
                    complemento='Apto 45',
                    bairro='Centro',
                    cidade='Rio de Janeiro',
                    estado='RJ',
                    cep='20040-020'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Endereço 2 criado: {endereco2}'))
                
                endereco3 = Endereco.objects.create(
                    rua='Rua Sete de Setembro',
                    numero='456',
                    bairro='Jardim América',
                    cidade='Belo Horizonte',
                    estado='MG',
                    cep='30130-000'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Endereço 3 criado: {endereco3}'))
                
                endereco4 = Endereco.objects.create(
                    rua='Avenida Brasil',
                    numero='2000',
                    complemento='Casa 5',
                    bairro='Jardim Botânico',
                    cidade='Curitiba',
                    estado='PR',
                    cep='80250-000'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Endereço 4 criado: {endereco4}'))
                
                endereco5 = Endereco.objects.create(
                    rua='Rua das Acácias',
                    numero='789',
                    bairro='Vila Nova',
                    cidade='São Paulo',
                    estado='SP',
                    cep='04567-890'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Endereço 5 criado: {endereco5}'))
                
                # ========== CADASTRAR USUÁRIOS E PERFIS ==========
                self.stdout.write('\n--- Cadastrando Usuários e Perfis ---')
                
                # Usuário 1 - João Silva
                usuario1 = Usuario.objects.create_user(
                    email='joao.silva@exemplo.com',
                    password='senha123',
                    first_name='João',
                    last_name='Silva'
                )
                perfil1 = Perfil.objects.create(
                    usuario=usuario1,
                    nome_social='João da Silva',
                    cpf='123.456.789-00',
                    data_nascimento=date(1990, 5, 15),
                    descricao='Adoro eventos culturais e encontros ao ar livre.',
                    genero='HOMEM_CIS',
                    is_pcd=False,
                    neurodiversidade=False,
                    endereco=endereco1
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuário criado: {usuario1.email}'))
                self.stdout.write(self.style.SUCCESS(f'  Perfil: {perfil1.nome_social} (Idade: {perfil1.idade} anos)'))
                
                # Usuário 2 - Maria Santos
                usuario2 = Usuario.objects.create_user(
                    email='maria.santos@exemplo.com',
                    password='senha456',
                    first_name='Maria',
                    last_name='Santos'
                )
                perfil2 = Perfil.objects.create(
                    usuario=usuario2,
                    endereco=endereco2,
                    nome_social='Maria Santos',
                    cpf='987.654.321-00',
                    data_nascimento=date(1992, 11, 25),
                    genero='MULHER_CIS',
                    descricao='Gosto de trilhas e aventuras!',
                    is_pcd=False,
                    neurodiversidade=True
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuário criado: {usuario2.email}'))
                self.stdout.write(self.style.SUCCESS(f'  Perfil: {perfil2.nome_social} (Idade: {perfil2.idade} anos)'))
                
                # Usuário 3 - Carlos Oliveira
                usuario3 = Usuario.objects.create_user(
                    email='carlos.oliveira@exemplo.com',
                    password='senha789',
                    first_name='Carlos',
                    last_name='Oliveira'
                )
                perfil3 = Perfil.objects.create(
                    usuario=usuario3,
                    data_nascimento=date(1988, 3, 10),
                    nome_social='Carlos',
                    genero='HOMEM_CIS',
                    is_pcd=True,
                    descricao='Apaixonado por música e arte.',
                    endereco=endereco3,
                    cpf='111.222.333-44'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuário criado: {usuario3.email}'))
                self.stdout.write(self.style.SUCCESS(f'  Perfil: {perfil3.nome_social} (Idade: {perfil3.idade} anos)'))
                
                # Usuário 4 - Ana Costa
                usuario4 = Usuario.objects.create_user(
                    email='ana.costa@exemplo.com',
                    password='senha321',
                    first_name='Ana',
                    last_name='Costa'
                )
                perfil4 = Perfil.objects.create(
                    usuario=usuario4,
                    data_nascimento=date(1995, 8, 20),
                    nome_social='Ana Costa',
                    genero='MULHER_TRANS',
                    descricao='Amo fotografia e natureza.',
                    endereco=endereco4,
                    cpf='555.666.777-88',
                    neurodiversidade=False,
                    is_pcd=False
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuário criado: {usuario4.email}'))
                self.stdout.write(self.style.SUCCESS(f'  Perfil: {perfil4.nome_social} (Idade: {perfil4.idade} anos)'))
                
                # Usuário 5 - Alex Santos (Não-binário)
                usuario5 = Usuario.objects.create_user(
                    email='alex.santos@exemplo.com',
                    password='senha654',
                    first_name='Alex',
                    last_name='Santos'
                )
                perfil5 = Perfil.objects.create(
                    usuario=usuario5,
                    data_nascimento=date(1998, 12, 5),
                    nome_social='Alex',
                    genero='NAO_BINARIO',
                    descricao='Entusiasta de tecnologia e games.',
                    endereco=endereco5,
                    cpf='999.888.777-66',
                    neurodiversidade=True,
                    is_pcd=False
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuário criado: {usuario5.email}'))
                self.stdout.write(self.style.SUCCESS(f'  Perfil: {perfil5.nome_social} (Idade: {perfil5.idade} anos)'))
                
                # ========== RESUMO ==========
                self.stdout.write('\n' + '='*50)
                self.stdout.write(self.style.SUCCESS('RESUMO DO CADASTRO:'))
                self.stdout.write(f'Endereços cadastrados: {Endereco.objects.count()}')
                self.stdout.write(f'Usuários cadastrados: {Usuario.objects.filter(is_superuser=False).count()}')
                self.stdout.write(f'Perfis cadastrados: {Perfil.objects.count()}')
                self.stdout.write('='*50)
                
                self.stdout.write(self.style.SUCCESS('\n✅ Dados cadastrados com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Erro ao cadastrar dados: {str(e)}'))
            raise

