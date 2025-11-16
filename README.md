# 🚀 Backend Simbora APP - Projeto Integrador (Padrão MTV)

## 💻 Visão Geral do Projeto

Este repositório contém o código **Backend** do **Simbora APP**, um projeto desenvolvido como parte do **Projeto Integrador** do curso de Programador de Sistemas. O projeto utiliza o framework Django.

O objetivo desta fase é estabelecer a base de dados e a lógica de negócios para o cadastro de usuários e perfis, renderizando as páginas web completas diretamente.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** Django
* **Padrão de Projeto:** MTV (Model-Template-View)
* **Banco de Dados:** SQLite (`db.sqlite3`)
* **Gerenciamento de Dependências:** `requirements.txt`

## 🧩 Estrutura Inicial do Repositório

O repositório está estruturado em *apps* do Django para modularizar as funcionalidades:

| Diretório/Arquivo | Descrição |
| :--- | :--- |
| `manage.py` | Utilitário de linha de comando do Django. |
| `requirements.txt` | Lista de bibliotecas Python necessárias. |
| `core/` | App principal do projeto. Contém configurações básicas e modelos fundamentais. |
| `perfil/` | App dedicada à gestão dos dados adicionais do perfil do usuário. |
| `simbora_app/` | Diretório principal do projeto Django (contém `settings.py`, `urls.py`). |
| `media/fotos_perfil/` | Configurado para armazenar arquivos de mídia (ex: fotos de perfil). |


## ⚙️ Instalação e Configuração

Para configurar o ambiente de desenvolvimento:

### 1. Pré-requisitos

* Python (versão 3.x)
* Git

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

# 🚀 Passo a passo para rodar o projeto localmente

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/simboralab/simbora.git
cd simbora
```

## 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

## 3️⃣ Ativar o ambiente virtual

### 🔹 Linux / macOS
```bash
source venv/bin/activate
```

### 🔹 Windows (PowerShell)
```bash
.\venv\Scripts\activate
```

## 4️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

## 5️⃣ Criar o arquivo `.env`

```bash
touch .env
```

Dentro do `.env`, coloque:

```env
# Chave secreta da criptografia do CPF
CPF_SECRET_KEY=troque_por_uma_chave_forte

# Outras variáveis...
DEBUG=True
```

## 6️⃣ Gerar nova chave secreta (opcional)

Abra o shell Python:

```bash
python
```

Gere a chave:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Cole no `.env`:

```env
CPF_SECRET_KEY=valor_gerado_aqui
```

## 7️⃣ Aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

## 8️⃣ Rodar o servidor

```bash
python manage.py runserver
```
