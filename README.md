# 🚀 LinkLocker API

Um microserviço de backend construído em 1 dia com FastAPI e SQLModel para resolver um problema real: salvar e gerenciar links para ler depois.

## O Problema

Quantas vezes você vê um link interessante (artigo, vídeo, produto) e o envia para si mesmo no WhatsApp ou Slack, apenas para perdê-lo para sempre? Esta API resolve isso, criando um "cofre" de links pessoal e centralizado.

## Tecnologias Utilizadas

* **Python 3.12+**
* **FastAPI:** Para a criação da API de alta performance.
* **SQLModel:** Para a modelagem de dados e comunicação com o banco (baseado em Pydantic e SQLAlchemy).
* **SQLite:** Para um banco de dados simples e baseado em arquivo.
* **Uvicorn:** Como servidor ASGI.

---

## 🚀 Como Rodar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPO.git](https://github.com/SEU-USUARIO/SEU-REPO.git)
    cd SEU-REPO
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor:**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Acesse a documentação interativa:**
    Abra seu navegador e vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📸 API em Ação

Aqui está a documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI:


*(DICA: Tire um print da sua tela do `/docs` mostrando todos os endpoints, suba no GitHub e coloque o link da imagem aqui)*

## 📚 Endpoints da API

A API fornece os seguintes endpoints CRUD:

* `POST /links` - Cria um novo link.
* `GET /links` - Lista todos os links (filtra por `?is_read=true/false`).
* `GET /links/{link_id}` - Obtém um link específico.
* `PUT /links/{link_id}/mark-as-read` - Marca um link como lido.
* `DELETE /links/{link_id}` - Apaga um link.