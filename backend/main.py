from typing import Union

# del pasado
from fastapi.middleware.cors import CORSMiddleware
import uvicorn # Para correrlo en local
from pydantic import BaseModel # recibir el body de la peticion
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends

from auraManager import AuraNeo4j
from neo4j import GraphDatabase


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],
)


aura = AuraNeo4j()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/login")
def user_login():
    return {"login": "ok"}

class UserComensal(BaseModel):
    userid: str
    password: str
    nombre: str
    apellido: str
    edad: int
    presupuesto_prom: float
    tieneVehiculo: bool
    fecha_registro: datetime
    imagen: str

@app.post("/user/signup/comensal")
def comensal_signup(user_comensal: UserComensal):
    aura.create_comensal(user_comensal.model_dump())
    return {"message": "Comensal creado exitosamente"}
    



class user_restaurante(BaseModel):
    userid: str
    password: str
    nombre: str
    rango_precios : str
    calificacion: float
    horario: str
    vende_alcohol: bool
    petFriendly: bool
    fecha_registro: datetime
    imagen: str


# Para correrlo en local
if __name__ == "__main__":
    uvicorn.run(app, port=8000)