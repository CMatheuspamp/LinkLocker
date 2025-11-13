# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from typing import List, Optional

# Meus imports (da pasta 'core')
from database import create_db_and_tables, get_session, Link

# Imports do bônus (pegar título)
import httpx
from bs4 import BeautifulSoup

# --- 1. Modelo de Entrada ---

# Schema SÓ pra entrada (POST). Valida o body.
# (Não é uma tabela, por isso 'table=True' não está aqui)
class LinkCreate(SQLModel):
    url: str
    title: Optional[str] = None


# --- 2. App FastAPI ---

app = FastAPI(
    title="LinkLocker API",
    description="Meu cofre de links.",
    version="0.1.0"
)

# Roda isso aqui quando a API liga
@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Chama a função lá do database.py


# --- 3. Endpoints ---

# Teste básico
@app.get("/")
def read_root():
    return {"message": "API no ar!"}


# --- CREATE ---
# response_model=Link força a saída. Bom pra docs.
@app.post("/links", response_model=Link)
def create_link(*, session: Session = Depends(get_session), link_data: LinkCreate):
    # session = Depends(get_session) -> Injeção de Dependência
    # link_data: LinkCreate -> Pega o JSON do body e valida
    
    # --- Bônus: Pegar título ---
    # Se o usuário não mandou um título...
    if not link_data.title:
        try: # try...except pq pode falhar (site 404, etc)
            # httpx vai na URL e baixa o HTML
            # follow_redirects=True (importante pra links encurtados)
            response = httpx.get(link_data.url, follow_redirects=True, timeout=5.0)
            
            # Se a página der erro (404, 500), isso aqui vai parar o código
            response.raise_for_status() 
            
            # BeautifulSoup (bs4) "lê" o texto HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tenta achar a tag <title>
            if soup.title and soup.title.string:
                # Pega o texto de dentro da tag e .strip() pra tirar espaços
                link_data.title = soup.title.string.strip() 
        
        except Exception as e:
            # Se der qualquer erro, só printa no meu console e segue em frente.
            # O link vai ser salvo sem título, sem problemas.
            print(f"Erro ao buscar título: {e}")
            pass # Continua a execução
    # --- Fim do Bônus ---

    # Converte o 'LinkCreate' (entrada) pro 'Link' (banco)
    db_link = Link.model_validate(link_data)
    
    session.add(db_link) # Prepara o INSERT
    session.commit() # Roda no banco
    session.refresh(db_link) # Pega os dados que o banco gerou (tipo o ID)
    
    return db_link


# --- READ (todos) ---
@app.get("/links", response_model=List[Link])
def read_links(
    *,
    session: Session = Depends(get_session),
    # Filtro opcional: /links?is_read=true
    is_read: Optional[bool] = None 
):
    statement = select(Link) # Prepara o SELECT *
    
    if is_read is not None:
        statement = statement.where(Link.is_read == is_read) # Adiciona o WHERE
        
    links = session.exec(statement).all() # Executa e pega todos
    return links


# --- READ (um só) ---
# {link_id} = path parameter
@app.get("/links/{link_id}", response_model=Link)
def read_link(*, session: Session = Depends(get_session), link_id: int):
    # .get() é o atalho pra buscar por ID (PK)
    link = session.get(Link, link_id)
    
    if not link:
        # Se não achar, manda 404.
        raise HTTPException(status_code=404, detail="Link não encontrado")
    
    return link


# --- UPDATE ---
@app.put("/links/{link_id}/mark-as-read", response_model=Link)
def mark_as_read(*, session: Session = Depends(get_session), link_id: int):
    # 1. Acha o link
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")
        
    # 2. Altera o campo
    link.is_read = True
    
    # 3. Salva (SQLModel vê que o obj mudou, prepara o UPDATE)
    session.add(link)
    session.commit()
    session.refresh(link)
    
    return link


# --- DELETE ---
@app.delete("/links/{link_id}")
def delete_link(*, session: Session = Depends(get_session), link_id: int):
    # 1. Acha
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")
        
    # 2. Deleta
    session.delete(link) # Prepara o DELETE
    session.commit() # Roda
    
    # Retorna uma msg de sucesso
    return {"ok": True, "detail": "Link apagado com sucesso"}