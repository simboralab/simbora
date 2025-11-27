// =============================================
// VALIDAÇÃO DE FORMULÁRIOS
// =============================================

// Validação em camadas:
// 1. HTML5 (required) - funciona mesmo com JS desabilitado
// 2. JavaScript - melhora UX com feedback customizado
// 3. Backend - validação final obrigatória no servidor

// Prevenir tooltips nativos do navegador, mas manter validação HTML5
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input[required], select[required]');

    inputs.forEach(input => {
        // Prevenir tooltip padrão, mas manter validação
        input.addEventListener('invalid', function (e) {
            // Prevenir tooltip nativo
            e.preventDefault();
            // Manter validação HTML5 funcionando
            this.setCustomValidity(' ');
        }, true);

        // Limpar validação customizada quando começar a digitar ou mudar
        if (input.type === 'checkbox') {
            input.addEventListener('change', function () {
                this.setCustomValidity('');
            });
        } else {
            input.addEventListener('input', function () {
                this.setCustomValidity('');
            });
        }
    });
});

// =============================================
// FUNÇÕES AUXILIARES DE VALIDAÇÃO
// =============================================

/**
 * Função para mostrar erro de validação
 * @param {string} inputId - ID do input que tem erro
 * @param {string} messageId - ID do elemento span que mostra a mensagem de erro
 * @param {string} message - Mensagem de erro a ser exibida
 */
function showError(inputId, messageId, message) {
    const input = document.getElementById(inputId);
    if (!input) return;

    const errorSpan = document.getElementById(messageId);
    const inputContainer = input.closest('.input-container');
    const checkboxContainer = input.closest('.checkbox-container');

    if (inputContainer) {
        inputContainer.classList.remove('success');
        inputContainer.classList.add('error');
        input.setAttribute('aria-invalid', 'true');
    }

    if (checkboxContainer) {
        checkboxContainer.classList.add('error');
        input.setAttribute('aria-invalid', 'true');
    }

    if (errorSpan) {
        errorSpan.textContent = message;
        errorSpan.classList.add('show');
    }
}

/**
 * Função para limpar validação de erro
 * @param {string} inputId - ID do input
 * @param {string} messageId - ID do elemento span de mensagem de erro
 */
function clearValidation(inputId, messageId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    const errorSpan = document.getElementById(messageId);
    const inputContainer = input.closest('.input-container');
    const checkboxContainer = input.closest('.checkbox-container');

    if (inputContainer) {
        inputContainer.classList.remove('error', 'success');
        input.removeAttribute('aria-invalid');
    }

    if (checkboxContainer) {
        checkboxContainer.classList.remove('error');
        input.removeAttribute('aria-invalid');
    }

    if (errorSpan) {
        errorSpan.textContent = '';
        errorSpan.classList.remove('show');
    }
}

// =============================================
// FUNÇÕES DE VALIDAÇÃO DE DADOS
// =============================================

/**
 * Valida formato de email
 * @param {string} email - Email a ser validado
 * @returns {boolean} - true se válido, false se inválido
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Valida senha (mínimo 8 caracteres)
 * TODO: Adicionar mais regras se necessário (maiúscula, número, caractere especial)
 * @param {string} password - Senha a ser validada
 * @returns {boolean} - true se válido, false se inválido
 */
function validatePassword(password) {
    return password.length >= 8;
}

/**
 * Valida se duas senhas coincidem
 * @param {string} password - Senha principal
 * @param {string} confirmPassword - Confirmação de senha
 * @returns {boolean} - true se coincidem, false se não coincidem
 */
function validatePasswordMatch(password, confirmPassword) {
    return password === confirmPassword && password.length > 0;
}

/**
 * Valida data de nascimento (deve ser no passado e maior de 18 anos)
 * @param {string} dateString - Data no formato YYYY-MM-DD
 * @returns {boolean} - true se válido, false se inválido
 */
function validateBirthDate(dateString) {
    if (!dateString) return false;

    const birthDate = new Date(dateString);
    const today = new Date();
    const age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        return (age - 1) >= 18;
    }

    return age >= 18;
}

// =============================================
// VALIDAÇÃO DO FORMULÁRIO DE CADASTRO
// =============================================

// Aguardar DOM estar pronto
document.addEventListener('DOMContentLoaded', function () {
    initValidation();
});

function initValidation() {
    const cadastroForm = document.querySelector('.cadastro-form form');
    if (!cadastroForm) return;

    // Obter referências dos campos
    const nome = document.getElementById('id_nome');
    const sobrenome = document.getElementById('id_sobrenome');
    const emailCadastro = document.getElementById('id_email_cadastro');
    const senhaCadastro = document.getElementById('id_senha_cadastro');
    const confirmarSenha = document.getElementById('id_confirmar_senha');
    const dataNascimento = document.getElementById('id_data_nascimento');
    const aceitarPoliticas = document.getElementById('id_aceitar_politicas');

    // =============================================
    // EXEMPLO: VALIDAÇÃO DE EMAIL (COMPLETA)
    // =============================================
    // Use este exemplo como referência para implementar outras validações

    if (emailCadastro) {
        // Validação quando o campo perde o foco (blur)
        emailCadastro.addEventListener('blur', function () {
            const email = this.value.trim();

            // Se tem valor e é inválido, mostrar erro
            if (email && !validateEmail(email)) {
                showError('id_email_cadastro', 'erro-email-cadastro', 'Por favor, insira um e-mail válido');
            } else {
                // Se está vazio ou válido, limpar erro
                clearValidation('id_email_cadastro', 'erro-email-cadastro');
            }
        });

        // Limpar erro quando começar a digitar novamente
        emailCadastro.addEventListener('input', function () {
            const inputContainer = this.closest('.input-container');
            if (inputContainer && inputContainer.classList.contains('error')) {
                clearValidation('id_email_cadastro', 'erro-email-cadastro');
            }
        });
    }

    // Validação do checkbox de aceitar políticas
    if (aceitarPoliticas) {
        aceitarPoliticas.addEventListener('change', function () {
            if (this.checked) {
                clearValidation('id_aceitar_politicas', 'erro-aceitar-politicas');
            }
        });
    }

    // =============================================
    // TODO: IMPLEMENTAR VALIDAÇÃO DE SENHA (COMPLETA)
    // =============================================
    // Siga o padrão do exemplo de email acima:

    if (senhaCadastro) {
        // 1. Adicionar event listener 'blur' para validar quando sair do campo
        senhaCadastro.addEventListener('blur', function () {
            const senha = this.value.trim();

            // 2. Usar a função validatePassword() para verificar se a senha é válida
            if (senha && !validatePassword(senha)) {
                // Chamar showError() se inválida
                showError('id_senha_cadastro', 'erro-senha-cadastro', 'A senha deve ter pelo menos 8 caracteres');
            } else {
                // clearValidation() se válida
                clearValidation('id_senha_cadastro', 'erro-senha-cadastro');
            }
        });

        // 4. Adicionar event listener 'input' para limpar erro ao digitar
        senhaCadastro.addEventListener('input', function () {
            const inputContainer = this.closest('.input-container');
            if (inputContainer && inputContainer.classList.contains('error')) {
                clearValidation('id_senha_cadastro', 'erro-senha-cadastro');
            }
        });
    }

    // =============================================
    // TODO: IMPLEMENTAR VALIDAÇÃO DE CONFIRMAÇÃO DE SENHA (COMPLETA)
    // =============================================
    // Similar à validação de senha, mas precisa comparar com a senha principal

    if (confirmarSenha) {
        // Dicas:
        // - Use validatePasswordMatch(senhaCadastro.value, confirmarSenha.value)
        if (senhaCadastro) {
            // 1. Adicionar event listener 'blur' no campo confirmarSenha
            confirmarSenha.addEventListener('blur', function () {
                const confirmarSenha = this.value.trim();
                const senha = senhaCadastro.value.trim();
                // 2. Verificar se as senhas coincidem
                if (confirmarSenha && !validatePasswordMatch(senha, confirmarSenha)) {
                    // 3. Se não coincidirem, chamar showError()
                    showError('id_confirmar_senha', 'erro-confirmar-senha', 'As senhas não coincidem');
                } else {
                    // 4. Se coincidirem ou vazio, chamar clearValidation()
                    clearValidation('id_confirmar_senha', 'erro-confirmar-senha');
                }
            });
            // - Considere validar em tempo real quando digitar (event 'input')
            confirmarSenha.addEventListener('input', function () {
                const inputContainer = this.closest('.input-container');
                if (inputContainer && inputContainer.classList.contains('error')) {
                    clearValidation('id_confirmar_senha', 'erro-confirmar-senha');
                }
            });
            // - Valide também quando a senha principal mudar
            senhaCadastro.addEventListener('input', function () {
                const inputContainer = confirmarSenha.closest('.input-container');
                if (inputContainer && inputContainer.classList.contains('error')) {
                    clearValidation('id_confirmar_senha', 'erro-confirmar-senha');
                }
            });
        }


        // =============================================
        // TODO: IMPLEMENTAR VALIDAÇÃO DE DATA DE NASCIMENTO (COMPLETA)
        // =============================================
        // INSTRUÇÕES:
        if (dataNascimento) {
            // 1. Criar event listener 'blur' no campo dataNascimento
            dataNascimento.addEventListener('blur', function () {
                // 2. Dentro do listener, obter o valor do campo (this.value)
                const data = this.value.trim();
                // 3. Verificar se a data existe e se é válida usando validateBirthDate()
                if (data && !validateBirthDate(data)) {
                    // 4. Se inválida, chamar showError() com:
                    //    - ID do input: 'id_data_nascimento'
                    //    - ID do span de erro: 'erro-data-nascimento'
                    //    - Mensagem: 'Você deve ter pelo menos 18 anos'
                    showError('id_data_nascimento', 'erro-data-nascimento', 'Você deve ter pelo menos 18 anos');
                    // 5. Se válida ou vazia, chamar clearValidation() com os mesmos IDs
                } else {
                    clearValidation('id_data_nascimento', 'erro-data-nascimento');
                }
            });

            // 6. Criar event listener 'change' para limpar erro quando a data mudar
            dataNascimento.addEventListener('change', function () {
                const inputContainer = this.closest('.input-container');
                // 7. No listener 'change', verificar se há erro e limpar usando clearValidation()
                if (inputContainer && inputContainer.classList.contains('error')) {
                    clearValidation('id_data_nascimento', 'erro-data-nascimento');
                }
            });
        }
        // 8. Seguir o mesmo padrão usado na validação de email acima
        // NOTA: A função validateBirthDate() já está disponível acima, apenas use-a

        // =============================================
        // TODO: IMPLEMENTAR VALIDAÇÃO DE NOME E SOBRENOME (COMPLETA)
        // =============================================
        // Validações básicas de campos de texto
        //
        // Dicas:
        if (nome) {
            // - Verificar se está vazio: !nome.value.trim()
            nome.addEventListener('blur', function () {
                const nomeValue = this.value.trim();
                if (!nomeValue) {
                    showError('id_nome', 'erro-nome', 'Por favor, insira seu nome');
                } else {
                    clearValidation('id_nome', 'erro-nome');
                }
            });
            nome.addEventListener('input', function () {
                const inputContainer = this.closest('.input-container');
                if (inputContainer && inputContainer.classList.contains('error')) {
                    clearValidation('id_nome', 'erro-nome');
                }
            });
        }
        if (sobrenome) {
            sobrenome.addEventListener('blur', function () {
                const sobrenomeValue = this.value.trim();
                if (!sobrenomeValue) {
                    showError('id_sobrenome', 'erro-sobrenome', 'Por favor, insira seu sobrenome');
                } else {
                    clearValidation('id_sobrenome', 'erro-sobrenome');
                }
            });
            sobrenome.addEventListener('input', function () {
                const inputContainer = this.closest('.input-container');
                if (inputContainer && inputContainer.classList.contains('error')) {
                    clearValidation('id_sobrenome', 'erro-sobrenome');
                }
            });
        }

        // - Verificar tamanho mínimo se necessário
        nome.addEventListener('blur', function () {
            const nomeValue = this.value.trim();
            if (nomeValue && nomeValue.length < 2) {
                showError('id_nome', 'erro-nome', 'O nome deve ter pelo menos 2 caracteres');
            }
        });
        sobrenome.addEventListener('blur', function () {
            const sobrenomeValue = this.value.trim();
            if (sobrenomeValue && sobrenomeValue.length < 2) {
                showError('id_sobrenome', 'erro-sobrenome', 'O sobrenome deve ter pelo menos 2 caracteres');
            }
        });

        // - Verificar caracteres especiais se necessário
        nome.addEventListener('blur', function () {
            const nomeValue = this.value.trim();
            const nameRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;
            if (nomeValue && !nameRegex.test(nomeValue)) {
                showError('id_nome', 'erro-nome', 'O nome contém caracteres inválidos');
            }
        });
        sobrenome.addEventListener('blur', function () {
            const sobrenomeValue = this.value.trim();
            const nameRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;
            if (sobrenomeValue && !nameRegex.test(sobrenomeValue)) {
                showError('id_sobrenome', 'erro-sobrenome', 'O sobrenome contém caracteres inválidos');
            }
        });

        // =============================================
        // VALIDAÇÃO NO SUBMIT DO FORMULÁRIO (COMPLETA)
        // =============================================
        // IMPORTANTE: Sempre validar todos os campos antes de enviar
        // Esta validação é a última camada antes do envio

        cadastroForm.addEventListener('submit', function (e) {
            let isValid = true;

            // Validar email 
            if (emailCadastro && (!emailCadastro.value.trim() || !validateEmail(emailCadastro.value.trim()))) {
                showError('id_email_cadastro', 'erro-email-cadastro', 'Por favor, insira um e-mail válido');
                isValid = false;
            }

            // TODO: Adicionar validação de nome 
            if (nome && (!nome.value.trim())) {
                showError('id_nome', 'erro-nome', 'Por favor, insira seu nome');
                isValid = false;
            }

            // TODO: Adicionar validação de sobrenome 
            if (sobrenome && (!sobrenome.value.trim())) {
                showError('id_sobrenome', 'erro-sobrenome', 'Por favor, insira seu sobrenome');
                isValid = false;
            }

            // TODO: Adicionar validação de senha 
            if (senhaCadastro && (!senhaCadastro.value.trim() || !validatePassword(senhaCadastro.value.trim()))) {
                showError('id_senha_cadastro', 'erro-senha-cadastro', 'A senha deve ter pelo menos 8 caracteres');
                isValid = false;
            }

            // TODO: Adicionar validação de confirmação de senha no submit
            if (confirmarSenha && senhaCadastro) {
                if (!validatePasswordMatch(senhaCadastro.value.trim(), confirmarSenha.value.trim())) {
                    showError('id_confirmar_senha', 'erro-confirmar-senha', 'As senhas não coincidem');
                    isValid = false;
                }
            }

            // TODO: Adicionar validação de data de nascimento no submit
            if (dataNascimento && (!dataNascimento.value.trim() || !validateBirthDate(dataNascimento.value.trim()))) {
                showError('id_data_nascimento', 'erro-data-nascimento', 'Você deve ter pelo menos 18 anos');
                isValid = false;
            }

            // Validar checkbox de aceitar políticas
            if (aceitarPoliticas && !aceitarPoliticas.checked) {
                showError('id_aceitar_politicas', 'erro-aceitar-politicas', 'Você deve aceitar os Termos de Serviço e a Política de Privacidade');
                isValid = false;
            }

            // Se houver erros, previne envio e focar no primeiro campo com erro
            if (!isValid) {
                e.preventDefault();
                const firstError = cadastroForm.querySelector('.error input, .error select, .checkbox-container.error input');
                if (firstError) {
                    firstError.focus();
                }
            }
        });
    }

    // =============================================
    // VALIDAÇÃO DO FORMULÁRIO DE LOGIN (COMPLETA)
    // =============================================

    const loginFormElement = document.querySelector('.login-form form');
    if (loginFormElement) {
        const emailLogin = document.getElementById('id_email_login');

        // Validação de email no login (mesmo padrão do cadastro)
        if (emailLogin) {
            emailLogin.addEventListener('blur', function () {
                const email = this.value.trim();
                if (email && !validateEmail(email)) {
                    showError('id_email_login', 'erro-email-login', 'Por favor, insira um e-mail válido');
                } else {
                    clearValidation('id_email_login', 'erro-email-login');
                }
            });

            emailLogin.addEventListener('input', function () {
                const inputContainer = this.closest('.input-container');
                if (inputContainer && inputContainer.classList.contains('error')) {
                    clearValidation('id_email_login', 'erro-email-login');
                }
            });
        }

        // TODO: Adicionar validação de senha no login 

        // Validação no submit do login
        const senhaLogin = document.getElementById('id_senha_login');

        loginFormElement.addEventListener('submit', function (e) {
            let isValid = true;

            // Validar email
            if (emailLogin && (!emailLogin.value.trim() || !validateEmail(emailLogin.value.trim()))) {
                showError('id_email_login', 'erro-email-login', 'Por favor, insira um e-mail válido');
                isValid = false;
            }

            // TODO: Adicionar validação de senha
            // INSTRUÇÕES:
            if (senhaLogin) {
                // 1. Verificar se o campo de senha existe e se está vazio
                senhaLogin.addEventListener('blur', function () {
                    const senha = this.value.trim();
                    if (!senha) {
                        showError('id_senha_login', 'erro-senha-login', 'Por favor, insira sua senha');
                    } else {
                        clearValidation('id_senha_login', 'erro-senha-login');
                    }
                });

                // 2. Se estiver vazio, chamar showError() com:
                //    - ID do input: 'id_senha_login'
                //    - ID do span de erro: 'erro-senha-login' (verificar se existe no HTML)
                //    - Mensagem de erro apropriada em português
                senhaLogin.addEventListener('blur', function () {
                    const senha = this.value.trim();
                    if (senha && !validatePassword(senha)) {
                        showError('id_senha_login', 'erro-senha-login', 'A senha deve ter pelo menos 8 caracteres');
                    } else {
                        clearValidation('id_senha_login', 'erro-senha-login');
                    }
                });

                senhaLogin.addEventListener('input', function () {
                    const inputContainer = this.closest('.input-container');
                    if (inputContainer && inputContainer.classList.contains('error')) {
                        clearValidation('id_senha_login', 'erro-senha-login');
                    }
                });
            }

            // 3. Se houver erro, definir isValid = false
            if (senhaLogin && !senhaLogin.value.trim()) {
                showError('id_senha_login', 'erro-senha-login', 'Por favor, insira sua senha');
                isValid = false;
            }

            // 4. Seguir o mesmo padrão usado na validação de email acima
            // NOTA: Verificar primeiro se o elemento span de erro existe no HTML antes de usar

            if (!isValid) {
                e.preventDefault();
                const firstError = loginFormElement.querySelector('.error input');
                if (firstError) {
                    firstError.focus();
                }
            }
        });
    }
}
// =============================================
// NOTAS IMPORTANTES PARA DESENVOLVEDORES
// =============================================
//
// 1. SEMPRE valide no backend também! A validação JavaScript é apenas para UX.
// 2. Use os IDs corretos dos elementos (verifique no HTML).
// 3. Use os IDs corretos dos spans de erro (ex: 'erro-email-cadastro').
// 4. Mantenha o padrão: validação no 'blur' e limpeza no 'input'.
// 5. Para validações em tempo real, use o evento 'input'.
// 6. Sempre valide no submit antes de enviar o formulário.
// 7. Use as funções auxiliares (validateEmail, validatePassword, etc.) quando disponíveis.
// 8. Mensagens de erro devem ser claras e em português.
// 9. Teste com JavaScript desabilitado - a validação HTML5 deve funcionar.
// 10. Teste acessibilidade com leitores de tela.