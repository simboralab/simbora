# 🤝 Guia de Contribuição

Contribuições são bem-vindas! Este guia irá ajudá-lo a contribuir com o projeto Simbora APP.

## 📋 Processo de Contribuição

### 1. Clone o repositório

```bash
git clone https://github.com/simboralab/simbora.git
cd simbora
```

### 2. Crie uma branch para sua feature

```bash
git checkout -b feature/nome-da-sua-feature
# ou
git checkout -b fix/nome-do-bug
```

**Convenções de nomeação de branches:**
- `feature/` para novas funcionalidades
- `fix/` para correções de bugs
- `docs/` para documentação
- `refactor/` para refatoração
- `test/` para testes

### 3. Faça suas alterações

- Desenvolva sua feature ou correção
- Certifique-se de seguir os padrões do projeto
- Execute os testes localmente:
```bash
make test
```

### 4. Commit suas alterações

```bash
git add .
git commit -m "feat: descrição da sua alteração"
```

#### Convenção de Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para documentação
- `refactor:` para refatoração de código
- `test:` para testes
- `chore:` para tarefas de manutenção
- `style:` para formatação de código (espaços, vírgulas, etc.)
- `perf:` para melhorias de performance

**Exemplos:**
```bash
git commit -m "feat: adiciona validação de CPF no formulário de cadastro"
git commit -m "fix: corrige erro ao salvar foto de perfil"
git commit -m "docs: atualiza README com instruções de instalação"
```

### 5. Envie suas alterações

```bash
git push origin feature/nome-da-sua-feature
```

### 6. Abra um Pull Request

1. Vá até o repositório no GitHub
2. Clique em **"New Pull Request"**
3. Selecione sua branch
4. Preencha o template do PR com:
   - Descrição clara das alterações
   - Motivação para a mudança
   - Screenshots (se aplicável)
   - Checklist de itens verificados

## ⚠️ Importante

### Por que usar Pull Requests?

É **fundamental** abrir um Pull Request para que possamos:

- ✅ **Garantir qualidade**: Revisar o código antes de integrar ao projeto
- ✅ **Revisão de código**: Permitir que outros desenvolvedores revisem e sugiram melhorias
- ✅ **Automações funcionando**: Os workflows do GitHub Actions executam testes automaticamente, validando que o código funciona corretamente antes do merge
- ✅ **Histórico e rastreabilidade**: Manter um histórico claro de mudanças e discussões
- ✅ **Facilita desfazer mudanças**: Se problemas forem detectados após a integração na `main`, é mais fácil identificar, reverter ou corrigir mudanças que foram feitas via PR do que commits diretos na branch principal

### Regras Importantes

- **Todas as contribuições devem ser feitas via Pull Request**
- Não faça commits diretamente na branch `main`
- Certifique-se de que os testes passam antes de abrir o PR
- Mantenha o código limpo e bem documentado
- Siga os padrões de código do projeto

## ✅ Checklist antes de abrir um PR

Antes de abrir seu Pull Request, certifique-se de que:

- [ ] Código testado localmente
- [ ] Testes passando (`make test`)
- [ ] Sem erros de lint
- [ ] Documentação atualizada (se necessário)
- [ ] Commits seguem a convenção
- [ ] Branch atualizada com `main` (se necessário)
- [ ] Código segue os padrões do projeto

## 🔍 Revisão de Código

- Os PRs serão revisados pelos mantenedores do projeto
- Feedback e sugestões podem ser solicitados
- Após aprovação, o PR será mergeado na branch `main`
- Se houver solicitações de mudanças, faça as alterações e atualize o PR

## 📚 Recursos Úteis

- [README Principal](../README.md) - Informações gerais do projeto
- [Makefile](../Makefile) - Comandos úteis para desenvolvimento
- [Documentação do Django](https://docs.djangoproject.com/) - Referência do framework

## 💡 Dicas

- Sempre teste suas alterações localmente antes de abrir um PR
- Mantenha os PRs focados em uma única funcionalidade ou correção
- Escreva mensagens de commit claras e descritivas
- Adicione comentários no código quando necessário
- Siga o estilo de código existente no projeto

## 🆘 Precisa de Ajuda?

Se tiver dúvidas sobre como contribuir:

1. Verifique a documentação do projeto
2. Abra uma issue no GitHub para discutir sua ideia
3. Entre em contato com os mantenedores do projeto

---

Obrigado por contribuir com o Simbora APP! 🚀

