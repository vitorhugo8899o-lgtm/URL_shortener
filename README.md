# 🔗 URL_shortener

[![Status do Projeto](https://img.shields.io/badge/Status-Em%20Produção-brightgreen)](https://front-url-vitor-hugos-projects-411fbd87.vercel.app/)

## 💥 Descrição do Projeto

O **URL_shortener** é um projeto desenvolvido com o objetivo de transformar URLs longas em links curtos e gerenciáveis.

Este projeto foi criado com o propósito de enriquecer o currículo, demonstrando habilidades completas de desenvolvimento **full-stack**, desde a criação de APIs seguras até a implementação de uma interface de usuário dinâmica.

## 🤠 Funcionalidades Principais

* **Encurtamento de URL:** Transforma qualquer URL longa em um link curto e exclusivo.
* **Autenticação Segura:** Login e cadastro de usuários para gerenciamento de links.
* **Gerenciamento de Links:** O usuário pode visualizar, acessar e excluir suas URLs encurtadas na seção "Minhas URLs".
* **Gerenciamento de Conta:** Opções para alteração de informações de conta e exclusão de conta.

## 🛠️ Tecnologias Utilizadas

O projeto é dividido em **Backend** (API) e **Frontend** (Interface do Usuário).

### ⚙️ Backend (API)

| Tecnologia | Descrição |
| :--- | :--- |
| **Python (FastAPI)** | Principal linguagem e framework para construção da API robusta e de alta performance. |
| **SQLAlchemy + Alembic** | ORM (Object-Relational Mapping) e ferramenta de migração de banco de dados. |
| **PyJWT** | Criação e verificação de JSON Web Tokens (JWT) para autenticação. |
| **Argon2** | Hash seguro para criptografar senhas de usuário. |
| **Hashids** | Lógica utilizada para gerar a parte única da URL encurtada, misturando a `SECRET_KEY` + a base. |
| **Pytest** | Framework de testes para garantir a funcionalidade dos endpoints. |

### ⚛️ Frontend (Interface)

| Tecnologia | Descrição |
| :--- | :--- |
| **React + Vite** | Biblioteca JavaScript e bundler para construção de interfaces rápidas e modernas. |
| **JavaScript** | Linguagem principal do desenvolvimento frontend. |
| **Tailwind CSS** | Framework de classes utilitárias para estilização rápida e responsiva. |
| **react-router-dom** | Gerenciamento das rotas da aplicação (navegação entre páginas). |
| **Axios** | Cliente HTTP para realizar requisições eficientes à API Backend. |

## 🌐 Deploy e Acesso

A aplicação está totalmente funcional e implantada online:

* **Acesso ao Frontend:** [https://front-url-vitor-hugos-projects-411fbd87.vercel.app/](https://front-url-vitor-hugos-projects-411fbd87.vercel.app/)
* **Plataforma Frontend:** Vercel
* **Plataforma Backend:** Render

---

## 💻 Como Acessar a Aplicação

1.  Acesse o link da aplicação: [https://front-url-vitor-hugos-projects-411fbd87.vercel.app/](https://front-url-vitor-hugos-projects-411fbd87.vercel.app/).
2.  Você será redirecionado para a página de **Login**. Se não possuir uma conta, crie uma.
3.  Após o cadastro/login, você acessará a página **principal** para encurtar URLs.
4.  As URLs criadas podem ser gerenciadas na seção **"Minhas URLs"** no menu de navegação, onde é possível acessá-las ou excluí-las.
5.  O menu de navegação também oferece opções para **alteração de informações de conta**, **exclusão de conta** e **logout**.

## ⚙️ Configuração e Execução Local (Backend Apenas)

**Atenção:** A execução local é voltada apenas para o **Backend**. O código do frontend não está disponível neste repositório.

### Pré-requisitos

* Python 3.x
* **Poetry** (Gerenciador de dependências Python)

### Passos para Configuração

1.  **Clone o Repositório:**
    ```bash
    git clone [LINK_DO_SEU_REPOSITORIO]
    cd URL_shortener # Ou o nome da pasta do seu projeto
    ```
2.  **Crie e Ative o Ambiente Virtual com Poetry:**
    ```bash
    poetry shell
    ```
3.  **Instale as Dependências:**
    ```bash
    poetry install
    ```
4.  **Execute a Aplicação:**
    ```bash
    task run
    ```

A aplicação estará rodando localmente no endereço: `http://127.0.0.1:8000` (porta 8000).

