const btnLogin = document.getElementById("btn-login");
const btnCadastro = document.getElementById("btn-cadastro");
const container = document.querySelector(".container");
const cadastroForm = document.querySelector(".cadastro-form");
const loginForm = document.querySelector(".login-form");

btnLogin.addEventListener("click", () => {
  container.classList.add("login-ativo");
  container.classList.remove("cadastro-ativo");
  cadastroForm.classList.remove("active");
  loginForm.classList.add("active");
});

btnCadastro.addEventListener("click", () => {
  container.classList.add("cadastro-ativo");
  container.classList.remove("login-ativo");
  loginForm.classList.remove("active");
  cadastroForm.classList.add("active");
});
