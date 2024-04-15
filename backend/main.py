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
    birthdate: datetime
    spending: float
    has_car: bool
    image: str

@app.post("/user/signup/diner")
def diner_signup(userDiner: UserDiner):
    #parsear el birthdate a date AAAA-MM-DD
    userDiner.birthdate = userDiner.birthdate.date()
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

@app.post("/user/signup/restaurant")
def restaurant_signup(userRestaurant: UserRestaurante):
    aura_response = aura.create_restaurant(userRestaurant.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "Restaurante ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el restaurante"}
    else:
        return {"status": 200, "message": "Restaurante creado exitosamente"}


class Location(BaseModel):
    country: str
    city: str
    zone: int
    is_dangerous: bool
    postal_code: int

@app.post("/creation/location")
def create_location(location: Location):
    aura_response = aura.create_location(location.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "La locacion ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando la locacion"}
    else:
        return {"status": 200, "message": "Locacion creada exitosamente"}


class Ingredient(BaseModel):
    name: str
    type: str
    calories: float
    is_vegan: bool
    has_gluten: bool

@app.post("/creation/ingredient")
def create_ingredient(ingredient: Ingredient):
    aura_response = aura.create_ingredient(ingredient.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "El ingrediente ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el ingrediente"}
    else:
        return {"status": 200, "message": "Ingrediente creado exitosamente"}

class Plate(BaseModel):
    name: str
    description: str
    is_vegan: bool
    avg_price: float
    has_alcohol: bool

@app.post("/creation/dish")
def create_dish(plate: Plate):
    aura_response = aura.create_dish(plate.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "El plato ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el plato"}
    else:
        return {"status": 200, "message": "Plato creado exitosamente"}

class Parking(BaseModel):
    parking_id: str
    price_per_hour: float
    capacity: int
    hadicap_spaces: int
    has_security: bool
    has_roof: bool

@app.post("/creation/parking")
def create_parking(parking: Parking):
    aura_response = aura.create_parking(parking.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "El parqueadero ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el parqueadero"}
    else:
        return {"status": 200, "message": "Parqueadero creado exitosamente"}



# Para correrlo en local
if __name__ == "__main__":
    uvicorn.run(app, port=8000)