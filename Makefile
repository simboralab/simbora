.PHONY: help install sync migrate makemigrations runserver shell createsuperuser test check show-env clean venv dev prod create-env create-env-force

# Variáveis
PYTHON := uv run python
MANAGE := $(PYTHON) manage.py
ENV_DEV := development
ENV_PROD := production

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)🚀 Simbora APP - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Instala/atualiza dependências usando uv sync
	@echo "$(BLUE)📦 Instalando dependências...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Dependências instaladas!$(NC)"

sync: install ## Alias para install

venv: ## Cria ambiente virtual (se necessário)
	@echo "$(BLUE)🔧 Criando ambiente virtual...$(NC)"
	uv venv
	@echo "$(GREEN)✅ Ambiente virtual criado!$(NC)"

# ===== COMANDOS DJANGO =====

migrate: ## Aplica migrações do banco de dados
	@echo "$(BLUE)🗄️  Aplicando migrações...$(NC)"
	$(MANAGE) migrate
	@echo "$(GREEN)✅ Migrações aplicadas!$(NC)"

makemigrations: ## Cria novas migrações
	@echo "$(BLUE)📝 Criando migrações...$(NC)"
	$(MANAGE) makemigrations
	@echo "$(GREEN)✅ Migrações criadas!$(NC)"

migrations: makemigrations migrate ## Cria e aplica migrações em sequência

runserver: ## Inicia o servidor de desenvolvimento (ambiente padrão: development)
	@echo "$(BLUE)🚀 Iniciando servidor Django...$(NC)"
	@echo "$(YELLOW)Ambiente: $(ENV_DEV)$(NC)"
	$(MANAGE) runserver

runserver-prod: ## Inicia o servidor em modo produção
	@echo "$(BLUE)🚀 Iniciando servidor Django em PRODUÇÃO...$(NC)"
	@echo "$(RED)⚠️  DEBUG=False, ambiente de produção$(NC)"
	SIMBORA_ENV=$(ENV_PROD) $(MANAGE) runserver

shell: ## Abre o shell interativo do Django
	@echo "$(BLUE)🐚 Abrindo Django shell...$(NC)"
	$(MANAGE) shell

shell-plus: ## Abre Django shell com IPython (se instalado)
	@echo "$(BLUE)🐚 Abrindo Django shell (IPython)...$(NC)"
	$(MANAGE) shell_plus || $(MANAGE) shell

createsuperuser: ## Cria um superusuário
	@echo "$(BLUE)👤 Criando superusuário...$(NC)"
	$(MANAGE) createsuperuser

# ===== VALIDAÇÃO E TESTES =====

check: ## Executa verificações do Django (check)
	@echo "$(BLUE)🔍 Executando verificações do Django...$(NC)"
	$(MANAGE) check
	@echo "$(GREEN)✅ Verificações concluídas!$(NC)"

check-deploy: ## Executa verificações específicas para deploy
	@echo "$(BLUE)🔍 Executando verificações para deploy...$(NC)"
	$(MANAGE) check --deploy
	@echo "$(GREEN)✅ Verificações concluídas!$(NC)"

test: ## Executa testes do projeto
	@echo "$(BLUE)🧪 Executando testes...$(NC)"
	SIMBORA_ENV=testing $(MANAGE) test
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

test-verbose: ## Executa testes com output verboso
	@echo "$(BLUE)🧪 Executando testes (verboso)...$(NC)"
	SIMBORA_ENV=testing $(MANAGE) test --verbosity=2

show-env: ## Mostra o ambiente atual e configurações
	@echo "$(BLUE)🔍 Verificando ambiente atual...$(NC)"
	$(MANAGE) show_env

env-check: show-env ## Alias para show-env

# ===== AMBIENTES =====

dev: ## Define ambiente como development (padrão)
	@echo "$(GREEN)🟡 Ambiente definido como DEVELOPMENT$(NC)"
	@echo "Execute: export SIMBORA_ENV=development"
	@echo "Ou use: make runserver"

prod: ## Define ambiente como production
	@echo "$(RED)🔴 Ambiente definido como PRODUCTION$(NC)"
	@echo "Execute: export SIMBORA_ENV=production"
	@echo "Ou use: make runserver-prod"

# ===== LIMPEZA =====

clean: ## Remove arquivos temporários e cache
	@echo "$(BLUE)🧹 Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

clean-db: ## Remove o banco de dados SQLite (⚠️ CUIDADO: apaga todos os dados!)
	@echo "$(RED)⚠️  Removendo banco de dados...$(NC)"
	rm -f db.sqlite3
	@echo "$(GREEN)✅ Banco de dados removido!$(NC)"

clean-all: clean clean-db ## Remove tudo (cache + banco de dados)

# ===== COLETAR ESTÁTICOS =====

collectstatic: ## Coleta arquivos estáticos para produção
	@echo "$(BLUE)📦 Coletando arquivos estáticos...$(NC)"
	SIMBORA_ENV=$(ENV_PROD) $(MANAGE) collectstatic --noinput
	@echo "$(GREEN)✅ Arquivos estáticos coletados!$(NC)"

# ===== GERAR CHAVES =====

generate-keys: ## Gera SECRET_KEY e FIELD_ENCRYPTION_KEY
	@echo "$(BLUE)🔑 Gerando chaves de segurança...$(NC)"
	@echo ""
	@echo "SECRET_KEY: $$($(PYTHON) contrib/secret_gen.py)"
	@$(PYTHON) -c "from cryptography.fernet import Fernet; print('FIELD_ENCRYPTION_KEY:', Fernet.generate_key().decode())"
	@echo ""
	@echo "$(GREEN)✅ Chaves geradas! Cole-as no arquivo .secrets.toml$(NC)"

create-env: ## Cria arquivo .env a partir do template
	@echo "$(BLUE)📝 Criando arquivo .env...$(NC)"
	@if [ -f .env ]; then \
		echo "$(YELLOW)⚠️  Arquivo .env já existe. Use 'make create-env-force' para sobrescrever$(NC)"; \
	else \
		cp contrib/env-sample.env .env; \
		echo "$(GREEN)✅ Arquivo .env criado!$(NC)"; \
		echo "$(BLUE)💡 Edite o arquivo .env conforme necessário$(NC)"; \
	fi

create-env-force: ## Cria/sobrescreve arquivo .env a partir do template
	@echo "$(BLUE)📝 Criando arquivo .env (forçando sobrescrita)...$(NC)"
	@cp contrib/env-sample.env .env
	@echo "$(GREEN)✅ Arquivo .env criado!$(NC)"
	@echo "$(BLUE)💡 Edite o arquivo .env conforme necessário$(NC)"

# ===== DESENVOLVIMENTO =====

format: ## Formata código com ruff (se disponível)
	@echo "$(BLUE)✨ Formatando código...$(NC)"
	uv run ruff format . || echo "$(YELLOW)⚠️  Ruff não disponível$(NC)"

lint: ## Verifica código com ruff (se disponível)
	@echo "$(BLUE)🔍 Verificando código...$(NC)"
	uv run ruff check . || echo "$(YELLOW)⚠️  Ruff não disponível$(NC)"

format-lint: format lint ## Formata e verifica código

# ===== INFORMAÇÕES =====

info: ## Mostra informações do projeto
	@echo "$(BLUE)📋 Informações do Projeto$(NC)"
	@echo ""
	@echo "Python: $$($(PYTHON) --version 2>&1)"
	@echo "Django: $$($(PYTHON) -c 'import django; print(django.get_version())')"
	@echo "Ambiente atual: $$(echo $${SIMBORA_ENV:-development})"
	@echo ""
	@echo "$(GREEN)✅ Informações exibidas!$(NC)"

# ===== SETUP INICIAL =====

setup: install migrate createsuperuser ## Setup completo: instala, migra e cria superusuário
	@echo ""
	@echo "$(GREEN)✅ Setup completo!$(NC)"
	@echo "$(BLUE)Execute 'make runserver' para iniciar o servidor$(NC)"

# Comando padrão
.DEFAULT_GOAL := help

