# 🚀 Backend Simbora APP - Projeto Integrador (Padrão MTV)

## 💻 Visão Geral do Projeto

Este repositório contém o código **Backend** do **Simbora APP**, um projeto desenvolvido como parte do **Projeto Integrador** do curso de Programador de Sistemas. O projeto utiliza o framework Django.

O objetivo desta fase é estabelecer a base de dados e a lógica de negócios para o cadastro de usuários e perfis, renderizando as páginas web completas diretamente.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework Web:** Django 5.1.14
* **Padrão de Projeto:** MTV (Model-Template-View)
* **Banco de Dados:** SQLite (`db.sqlite3`)
* **Gerenciamento de Dependências:** `uv` com `pyproject.toml` (padrão moderno Python)
* **Gerenciamento de Configurações:** Dynaconf (múltiplos ambientes, validação automática)

## 🧩 Estrutura Inicial do Repositório

O repositório está estruturado em *apps* do Django para modularizar as funcionalidades:

| Diretório/Arquivo | Descrição |
| :--- | :--- |
| `manage.py` | Utilitário de linha de comando do Django. |
| `Makefile` | Comandos úteis para desenvolvimento (30+ comandos disponíveis). |
| `pyproject.toml` | Arquivo de configuração do projeto com todas as dependências (gerenciado pelo `uv`). |
| `uv.lock` | Arquivo de lock das dependências com versões exatas (gerado automaticamente pelo `uv`). |
| `config.py` | Configuração principal do Dynaconf (validações e ambientes). |
| `settings.toml` | Configurações por ambiente (development, production, testing). |
| `.secrets.toml` | Secrets locais (chaves secretas - **não versionado no Git**). |
| `.secrets.toml.example` | Template de exemplo para secrets (versionado no Git). |
| `core/` | App principal do projeto. Contém configurações básicas e modelos fundamentais. |
| `perfil/` | App dedicada à gestão dos dados adicionais do perfil do usuário. |
| `simbora_app/` | Diretório principal do projeto Django (contém `settings.py`, `urls.py`). |
| `media/fotos_perfil/` | Configurado para armazenar arquivos de mídia (ex: fotos de perfil). |


## ⚙️ Instalação e Configuração

Para configurar o ambiente de desenvolvimento:

### 1. Pré-requisitos

* Python (versão 3.12 ou superior)
* Git
* `uv` - Gerenciador rápido de pacotes Python

#### Instalando o `uv`

**Linux / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Ou via pip:**
```bash
pip install uv
```

Para mais informações, consulte: https://github.com/astral-sh/uv

## 🧑‍💻 Autores e Equipe

O time de Back-end do Projeto Integrador é composto pelos seguintes membros (em ordem alfabética):

* **Alison**
* **Geovane**
* **Julia Gonçalves**
* **Julia Martins**
* **Katarina**
* **Sidney**

**Curso:** Programador de Sistemas
**Instituição:** SENAC em parceria com Serasa (Programa Transforme-se)

# 🚀 Quick Start

Para começar rapidamente:

```bash
# 1. Clonar repositório
git clone https://github.com/simboralab/simbora.git
cd simbora

# 2. Instalar dependências
make install

# 3. Configurar secrets
cp .secrets.toml.example .secrets.toml
make generate-keys  # Copie as chaves geradas para .secrets.toml

# 4. Setup completo
make setup

# 5. Rodar servidor
make runserver
```

---

# 📖 Passo a passo detalhado

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/simboralab/simbora.git
cd simbora
```

## 2️⃣ Instalar dependências com `uv`

O `uv` gerencia automaticamente o ambiente virtual e as dependências através do `pyproject.toml`. Você pode usar o `uv` de duas formas:

### Opção A: Usar `uv sync` + `uv run` (recomendado)

```bash
# Sincronizar dependências do pyproject.toml (cria ambiente virtual automaticamente)
uv sync

# Executar comandos diretamente (não precisa ativar ambiente virtual)
uv run python manage.py migrate
uv run python manage.py runserver
```

### Opção B: Criar e ativar ambiente virtual manualmente

```bash
# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
# Linux / macOS:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\activate

# Sincronizar dependências
uv sync
```

## 3️⃣ Comandos úteis do `uv`

```bash
# Adicionar uma nova dependência (atualiza pyproject.toml automaticamente)
uv add nome-do-pacote

# Adicionar dependência com versão específica
uv add "nome-do-pacote==1.2.3"

# Adicionar dependência de desenvolvimento
uv add --dev nome-do-pacote

# Remover uma dependência (atualiza pyproject.toml automaticamente)
uv remove nome-do-pacote

# Sincronizar dependências do pyproject.toml (instala/atualiza conforme necessário)
uv sync

# Atualizar todas as dependências para versões mais recentes
uv sync --upgrade

# Ver dependências instaladas
uv pip list
```

## 4️⃣ Configurar Secrets e Ambiente

O projeto usa **Dynaconf** para gerenciar configurações de forma pythonica e segura, com suporte a múltiplos ambientes.

### 4.1 Criar o arquivo `.secrets.toml`

**⚠️ IMPORTANTE:** O `.secrets.toml` **NÃO vai para o repositório**. Cada desenvolvedor precisa criar o seu próprio a partir do template.

```bash
# Copie o template (que está no repositório)
cp .secrets.toml.example .secrets.toml

# O arquivo .secrets.toml será criado localmente e não será commitado
```

### 4.2 Gerar chaves necessárias

**Usando Makefile (recomendado):**
```bash
make generate-keys
```

**Ou usando comandos diretos:**
```bash
uv run python -c "from cryptography.fernet import Fernet; print('SECRET_KEY:', Fernet.generate_key().decode()); print('FIELD_ENCRYPTION_KEY:', Fernet.generate_key().decode())"
```

Copie as chaves geradas e cole no arquivo `.secrets.toml`.

### 4.3 Editar `.secrets.toml`

Abra o arquivo `.secrets.toml` e cole as chaves geradas:

```toml
[default]
secret_key = "cole-a-chave-secret-key-aqui"
field_encryption_key = "cole-a-chave-field-encryption-key-aqui"

[development]
secret_key = "cole-a-chave-secret-key-aqui"
field_encryption_key = "cole-a-chave-field-encryption-key-aqui"
```

**⚠️ IMPORTANTE:** 
- O arquivo `.secrets.toml` está no `.gitignore` e **não será commitado**
- Cada desenvolvedor cria seu próprio `.secrets.toml` a partir do template `.secrets.toml.example`
- Se o `.env` não existir, o Dynaconf usa automaticamente o `.secrets.toml`
- Mantenha suas chaves seguras e nunca commite o `.secrets.toml`!

### 4.4 Ambientes Disponíveis

O projeto suporta 3 ambientes:

- **development** (padrão): `DEBUG=True`, mais detalhes de erro
- **production**: `DEBUG=False`, otimizado para produção
- **testing**: Configurações para testes automatizados

**Nota:** O arquivo `.env` é opcional. O Dynaconf prioriza variáveis de ambiente com prefixo `SIMBORA_*` se você quiser usar.

### 4.5 Criar arquivo `.env` (Opcional)

O arquivo `.env` é **opcional** com Dynaconf, mas pode ser útil para algumas configurações. O Dynaconf carrega o `.env` automaticamente se existir.

**Usando Makefile (recomendado):**
```bash
make create-env        # Cria .env se não existir
make create-env-force  # Cria/sobrescreve .env
```

**Ou manualmente:**
```bash
# Copiar o template
cp contrib/env-sample.env .env

# Ou criar do zero
touch .env
```

**Formato do `.env` com Dynaconf:**
```env
# Ambiente (development, production, testing)
SIMBORA_ENV=development

# Secrets (opcional - use .secrets.toml se possível)
SIMBORA_SECRET_KEY=sua-chave-aqui
SIMBORA_FIELD_ENCRYPTION_KEY=sua-chave-fernet-aqui

# Configurações Django (opcional)
SIMBORA_DEBUG=True
SIMBORA_ALLOWED_HOSTS=["127.0.0.1", "localhost"]
```

**⚠️ IMPORTANTE:** 
- O `.env` está no `.gitignore` e **não será commitado**
- O Dynaconf prioriza: variáveis de ambiente > `.secrets.toml` > `settings.toml` > `.env`
- Para secrets, prefira usar `.secrets.toml` (mais seguro e organizado)

### 4.6 Sobre o Dynaconf

O projeto usa **Dynaconf** para gerenciar configurações de forma pythonica:

- ✅ **Validação automática** de secrets obrigatórios
- ✅ **Tipagem automática** (boolean, list, etc.)
- ✅ **Múltiplos ambientes** (development, production, testing)
- ✅ **Hierarquia de configurações** (arquivos TOML + variáveis de ambiente)
- ✅ **Código limpo** sem funções auxiliares manuais

**Trocar de ambiente:**
```bash
# Development (padrão)
unset SIMBORA_ENV
make runserver

# Production
export SIMBORA_ENV=production
make runserver-prod

# Verificar ambiente atual
make show-env
```

## 5️⃣ Aplicar migrações

### Usando Makefile (recomendado)

```bash
make migrations        # Cria e aplica migrações
# OU
make makemigrations    # Apenas cria migrações
make migrate          # Apenas aplica migrações
```

### Usando comandos diretos

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## 6️⃣ Rodar o servidor

### Usando Makefile (recomendado)

```bash
make runserver        # Desenvolvimento (padrão)
make runserver-prod   # Produção
```

### Usando comandos diretos

**Desenvolvimento (padrão):**
```bash
uv run python manage.py runserver
```

**Produção:**
```bash
export SIMBORA_ENV=production
uv run python manage.py runserver
# Ou em uma linha:
SIMBORA_ENV=production uv run python manage.py runserver
```

### Validar ambiente atual

```bash
# Usando Makefile (recomendado)
make show-env

# Ou usando comandos diretos
uv run python manage.py show_env
```

O servidor estará disponível em `http://127.0.0.1:8000/` ou `http://localhost:8000/`

## 🔍 Makefile - Comandos Úteis

O projeto inclui um **Makefile** completo com 30+ comandos úteis para facilitar o desenvolvimento.

### Ver todos os comandos

```bash
make help
```

### Comandos Principais

| Comando | Descrição |
| :--- | :--- |
| `make setup` | Setup completo: instala dependências, migra e cria superusuário |
| `make runserver` | Inicia servidor em desenvolvimento |
| `make runserver-prod` | Inicia servidor em produção |
| `make migrations` | Cria e aplica migrações |
| `make show-env` | Mostra ambiente atual e configurações |
| `make check` | Executa verificações do Django |
| `make test` | Executa testes |
| `make generate-keys` | Gera SECRET_KEY e FIELD_ENCRYPTION_KEY |
| `make clean` | Limpa cache e arquivos temporários |
| `make info` | Mostra informações do projeto |

### Exemplos Práticos

```bash
# Setup inicial completo
make setup

# Desenvolvimento diário
make runserver
make migrations
make createsuperuser
make show-env

# Produção
make runserver-prod
make collectstatic
make check-deploy

# Manutenção
make clean
make generate-keys
make info
```

### Comandos Disponíveis

Execute `make help` para ver a lista completa de todos os comandos disponíveis.

## 📝 Informações Adicionais

### Sobre o `uv` e `pyproject.toml`

- **Gerenciamento de dependências**: Todas as dependências são gerenciadas através do `pyproject.toml`
- **Vantagens do `uv`**: Instalação muito mais rápida que `pip`, gerencia ambientes virtuais automaticamente
- **Sem ambiente virtual**: Use `uv run` para executar comandos sem precisar ativar o ambiente virtual
- **Lock file**: O arquivo `uv.lock` garante versões exatas das dependências (recomendado versionar no Git)
- **Adicionar dependências**: Use `uv add` para adicionar novas dependências - o `pyproject.toml` será atualizado automaticamente
- **Sincronização**: Use `uv sync` ou `make install` para instalar/atualizar dependências

### Sobre o Makefile

O projeto inclui um **Makefile** completo com comandos úteis. Use `make help` para ver todos os comandos disponíveis.

**Principais vantagens:**
- ✅ Comandos mais curtos e fáceis de lembrar
- ✅ Padronização entre desenvolvedores
- ✅ Integração automática com `uv run`
- ✅ Suporte a múltiplos ambientes

### Segurança

- ⚠️ **Nunca commite** o arquivo `.secrets.toml` (já está no `.gitignore`)
- 🔑 Use `make generate-keys` para gerar chaves seguras
- 🔒 Em produção, use variáveis de ambiente ou um gerenciador de secrets
- ✅ O Dynaconf valida automaticamente se os secrets estão definidos

### Troubleshooting

**Erro: "ModuleNotFoundError: No module named 'django'"**
```bash
# Certifique-se de usar uv run ou make
make install
make runserver
```

**Erro: "Bad Request (400)" em produção**
```bash
# Verifique se ALLOWED_HOSTS está configurado
make show-env
# Configure via variável de ambiente ou settings.toml
```

**Erro: "FIELD_ENCRYPTION_KEY defined incorrectly"**
```bash
# Gere uma nova chave Fernet válida
make generate-keys
# Cole no .secrets.toml
```
