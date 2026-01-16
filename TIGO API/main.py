from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Slipknot1997@localhost/sistema_soporte"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    direccion = Column(String(255))
    correo = Column(String(100), index=True)

class TicketDB(Base):
    __tablename__ = "tickets"
    id_tickets = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150))
    descripcion = Column(Text)
    estado = Column(Enum('abierto', 'en proceso', 'cerrado'), default='abierto')
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))

class UsuarioCreate(BaseModel):
    nombre: str
    direccion: str
    correo: EmailStr

class TicketCreate(BaseModel):
    titulo: str
    descripcion: str
    id_usuario: int

app = FastAPI()

@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    try:
        db_user = UsuarioDB(**usuario.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error de base de datos: {str(e)}")
    finally:
        db.close()
@app.post("/tickets/")
def crear_ticket(ticket: TicketCreate):
    db = SessionLocal()
    db_ticket = TicketDB(**ticket.dict())
    db.add(db_ticket)
    try:
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/tickets/{ticket_id}")
def obtener_seguimiento(ticket_id: int):
    db = SessionLocal()
    ticket = db.query(TicketDB).filter(TicketDB.id_tickets == ticket_id).first()
    db.close()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return {"id": ticket.id_tickets, "titulo": ticket.titulo, "estado": ticket.estado}