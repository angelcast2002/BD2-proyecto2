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
    return {"ANS": "HOLA ANGEL TONOTO"}

@app.get("/user/login")
def user_login():
    return {"login": "ok"}

class UserDiner(BaseModel):
    user_id: str
    password: str
    name: str
    lastname: str
    birthdate: int
    spending: float
    has_car: bool
    image: str

@app.post("/user/signup/diner")
def diner_signup(userDiner: UserDiner):
    aura_response = aura.create_diner(userDiner.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "El usuario ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el usuario"}
    else:
        return {"status": 200, "message": "Usuario creado exitosamente"}
    
class UserRestaurante(BaseModel):
    user_id: str
    password: str
    name: str
    prices : str
    rating: float
    schedule: str
    sells_alcohol: bool
    petFriendly: bool
    imagen: str
    pass

@app.post("/user/signup/restaurant")
def restaurant_signup(userRestaurant: UserRestaurante):
    aura_response = aura.create_restaurant(userRestaurant.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "Restaurante ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el restaurante"}
    else:
        return {"status": 200, "message": "Restaurante creado exitosamente"}

# Para correrlo en local
if __name__ == "__main__":
    uvicorn.run(app, port=8000)