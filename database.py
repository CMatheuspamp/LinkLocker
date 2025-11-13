# database.py
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session

# --- 1. Modelo de Dados ---

# O "molde" do meu link.
# table=True -> vira tabela no DB.
class Link(SQLModel, table=True):
    # Opcional pq o banco que gera. PK.
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # index=True pra busca rápida
    url: str = Field(index=True) 
    
    title: Optional[str] = None # Pode ser nulo
    is_read: bool = Field(default=False) # Começa como falso
    
    # default_factory -> chama a função (pega a hora certa)
    # não é default=... (que usaria a mesma hora sempre)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# --- 2. Conexão com o Banco ---

sqlite_file_name = "links.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# A engine. echo=True pra ver o SQL no terminal (debug)
engine = create_engine(sqlite_url, echo=True)


# --- 3. Funções "Helper" ---

# Roda no startup, cria as tabelas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Injeção de dependência. Gera a sessão (conexão).
def get_session():
    # 'with' garante que a sessão fecha sozinha no final.
    with Session(engine) as session:
        # 'yield' entrega a sessão pro endpoint
        yield session
        # ...quando o endpoint acaba, o 'with' fecha ela.