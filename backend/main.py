from typing import Union

# del pasado
from fastapi.middleware.cors import CORSMiddleware
import uvicorn # Para correrlo en local
from pydantic import BaseModel # recibir el body de la peticion
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends

from auraManager import AuraNeo4j, sistema_recomendacion
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

# User
@app.get("/user/login")
def user_login(user_id: str, password: str):
    aura_response = aura.user_login(user_id, password)
    if aura_response == 404:
        return {"status": 404, "message": "Credenciales incorrectas"}
    else:
        return {"status": 200, "message": "Login exitoso", "role": aura_response[0]}
    
@app.get("/user/get")
def get_user(user_id: str):
    aura_response = aura.get_user_info(user_id)
    if aura_response == 404:
        return {"status": 404, "message": "Usuario no existe"}
    else:
        return aura_response

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

class updateDiner(BaseModel):
    name: str
    lastname: str
    spending: float
    has_car: bool
    image: str

class updateRestaurant(BaseModel):
    name: str
    prices : str
    schedule: str
    sells_alcohol: bool
    petFriendly: bool
    imagen: str

@app.put("/user/update")
def update_user(user_id: str, user: Union[updateDiner, updateRestaurant]):
    aura_response = aura.update_user_info(user_id, user.model_dump())
    if aura_response == 404:
        return {"status": 404, "message": "Usuario no existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error actualizando el usuario"}
    else:
        return {"status": 200, "message": "Usuario actualizado exitosamente"}
    
@app.delete("/user/delete")
def delete_user(user_id: str):
    aura_response = aura.delete_user(user_id)
    if aura_response == 404:
        return {"status": 404, "message": "Usuario no existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error eliminando el usuario"}
    else:
        return {"status": 200, "message": "Usuario eliminado exitosamente"}

class Location(BaseModel):
    country: str
    city: str
    zone: int
    is_dangerous: bool
    postal_code: int

# Creation

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
    handicap_friendly: int
    has_security: bool
    is_covered: bool

@app.post("/creation/parking")
def create_parking(parking: Parking):
    aura_response = aura.create_parking(parking.model_dump())
    if aura_response == 409:
        return {"status": 409, "message": "El parqueadero ya existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error creando el parqueadero"}
    else:
        return {"status": 200, "message": "Parqueadero creado exitosamente"}
    
# Search

@app.get("/get/restaurant")
def search_restaurant(restaurant_id: str):
    aura_response = aura.search_restaurant(restaurant_id)
    if aura_response == 404:
        return {"status": 404, "message": "El restaurante no existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error obteniendo el restaurante"}
    else:
        return aura_response


@app.get("/get/ingredient")
def search_ingredient(ingredient_id: str):
    aura_response = aura.search_ingredient(ingredient_id)
    if aura_response == 404:
        return {"status": 404, "message": "El ingrediente no existe"}
    else:
        return aura_response
    
@app.get("/get/dish")
def search_dish(dish_id: str):
    aura_response = aura.search_dish(dish_id)
    if aura_response == 404:
        return {"status": 404, "message": "El plato no existe"}
    else:
        return aura_response
    
@app.get("/get/location")
def search_location(city: str, zone: int):
    aura_response = aura.search_location(city, zone)
    if aura_response == 404:
        return {"status": 404, "message": "La locacion no existe"}
    else:
        return aura_response
    
@app.get("/get/location/all")
def get_all_locations():
    aura_response = aura.get_all_location_zones()
    return {"status": 200, "message": "Zonas obtenidas exitosamente", "data": aura_response}

@app.get("/get/parking")
def search_parking(parking_id: str):
    aura_response = aura.search_parking(parking_id)
    if aura_response == 404:
        return {"status": 404, "message": "El parqueadero no existe"}
    else:
        return aura_response

@app.get("/get/ingredientsAll")
def get_all_ingredients():
    aura_response = aura.get_all_ingredients()
    return {"status": 200, "message": "Ingredientes obtenidos exitosamente", "data": aura_response}

@app.get("/get/dishesAll")
def get_all_dishes():
    aura_response = aura.get_all_dishes()
    return {"status": 200, "message": "Platos obtenidos exitosamente", "data": aura_response}

@app.get("/get/restaurantsAll")
def get_all_restaurants():
    aura_response = aura.get_all_restaurants()
    return {"status": 200, "message": "Restaurantes obtenidos exitosamente", "data": aura_response}

@app.get("/get/parkingsAll")
def get_all_parkings():
    aura_response = aura.get_all_parkings()
    return {"status": 200, "message": "Parqueaderos obtenidos exitosamente", "data": aura_response}

# Diner

class visito(BaseModel):
    user_id: str
    restaurant_id: str
    dishes: list
    date: datetime
    total: float
    rating: float
    comment: str

@app.post("/diner/visit")
def create_visito(visito: visito):
    
    aura_response = aura.create_visit(visito.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la visita"}
    else:
        return {"status": 200, "message": "Visita creada exitosamente"}
    
class diner_on_restaurant(BaseModel):
    diner_id: str
    restaurant_id: str
    its_fav: bool
    user_likes: bool
    comments: str

@app.post("/diner/on_restaurant")
def diner_on_restaurant(diner_on_restaurant: diner_on_restaurant):
    aura_response = aura.diner_on_restaurant(diner_on_restaurant.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la relacion"}
    else:
        return {"status": 200, "message": "Relacion creada exitosamente"}

class DinerLocation(BaseModel):
    diner_id: str
    street: str
    avenue: str
    number: str
    community: str
    reference: str
    zone: int

@app.post("/diner/location")
def diner_location(dinerLocation: DinerLocation):
    aura_response = aura.diner_lives_in(dinerLocation.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la locacion"}
    else:
        return {"status": 200, "message": "Locacion creada exitosamente"}
    
@app.delete("/diner/visit")
def delete_diner_on_restaurant(diner_id: str, restaurant_id: str):
    aura_response = aura.delete_diner_visit(diner_id, restaurant_id)
    if aura_response == 404:
        return {"status": 404, "message": "La relacion no existe"}
    else:
        return {"status": 200, "message": "Relacion eliminada exitosamente"}
    
# Restaurant

class restaurant_sells(BaseModel):
    restaurant_id: str
    dish_id: str
    price: float
    sell_time: str
    cost: float

@app.post("/restaurant/sells")
def restaurant_sells(restaurant_sells: restaurant_sells):
    aura_response = aura.restaurant_sells(restaurant_sells.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la relacion"}
    else:
        return {"status": 200, "message": "Relacion creada exitosamente"}       

@app.get("/restaurant/dishes")
def get_dishes(restaurant_id: str):
    aura_response = aura.search_sells_relationship(restaurant_id)
    if aura_response == 404:
        return {"status": 404, "message": "El restaurante no existe"}
    else:
        return {"status": 200, "message": "Platos obtenidos exitosamente", "data": aura_response}

class RestaurantLocation(BaseModel):
    restaurant_id: str
    street: str
    avenue: str
    number: str
    community: str
    reference: str
    zone: int

@app.post("/restaurant/location")
def restaurant_location(restaurantLocation: RestaurantLocation):
    aura_response = aura.restaurant_located_in(restaurantLocation.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la locacion"}
    else:
        return {"status": 200, "message": "Locacion creada exitosamente"}
    
class restaurant_parking(BaseModel):
    restaurant_id: str
    parking_id: str
    vallet_parking: bool
    free_hours: int
    exclusive: bool


@app.get("/restaurant/location")
def get_restaurant_location(restaurant_id: str):
    aura_response = aura.serach_restaurant_location(restaurant_id)
    if aura_response == 404:
        return {"status": 404, "message": "El restaurante no existe o no tiene locacion asociada"}
    else:
        return {"status": 200, "message": "Locacion obtenida exitosamente", "data": aura_response}

@app.post("/restaurant/parking")
def restaurant_parking(restaurant_parking: restaurant_parking):
    aura_response = aura.restaurant_has_parking(restaurant_parking.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la relacion"}
    else:
        return {"status": 200, "message": "Relacion creada exitosamente"}

class restaurantDelivery(BaseModel):
    restaurant_id: str
    zone: int
    price: float
    time: str
    own_delivery: bool

@app.post("/restaurant/delivery")
def restaurant_delivery(delivery: restaurantDelivery):
    aura_response = aura.restaurant_has_delivery(delivery.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la relacion"}
    else:
        return {"status": 200, "message": "Delivery creado exitosamente"}
    
@app.get("/restaurant/comments")
def get_restaurant_comments(restaurant_id: str):
    aura_response = aura.get_restaurant_reviews(restaurant_id)
    if aura_response == 404:
        return {"status": 404, "message": "El restaurante no tiene comentarios"}
    else:
        # 
        return {"status": 200, "message": "Comentarios obtenidos exitosamente", "data": aura_response}

# Parking
@app.get("/parking/location")
def get_parking_location(parking_id: str):
    aura_response = aura.get_parking_location(parking_id)
    if aura_response == 404:
        return {"status": 404, "message": "El parqueadero no existe o no tiene locacion asociada"}
    else:
        return {"status": 200, "message": "Locacion obtenida exitosamente", "data": aura_response}

class parkingLocation(BaseModel):
    parking_id: str
    street: str
    avenue: str
    number: str
    community: str
    reference: str
    zone: int
@app.post("/parking/location")
def parking_location(parkingLocation: parkingLocation):
    aura_response = aura.parking_in(parkingLocation.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la locacion"}
    else:
        return {"status": 200, "message": "Locacion creada exitosamente"}

# Dish

class dish_opinion(BaseModel):
    dish_id: str
    diner_id: str
    favorite: bool
    likes: bool
    comment: str


@app.post("/dish/opinion")
def dish_opinion(dish_opinion: dish_opinion):
    aura_response = aura.diner_opinion(dish_opinion.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la opinion"}
    else:
        return {"status": 200, "message": "Opinion creada exitosamente"}
    
@app.get("/dish/ingredients")
def get_ingredients(dish_id: str):
    aura_response = aura.get_ingredients(dish_id)
    if aura_response == 404:
        return {"status": 404, "message": "El plato no existe"}
    else:
        return aura_response

class ingredient_plate(BaseModel):
    ingredient_id: str
    dish_id: str
    quantity: float
    cook_method: str
    cook_time: str

@app.post("/dish/ingredient")
def dish_ingredient(ingredient_plate: ingredient_plate):
    aura_response = aura.dish_has_ingredient(ingredient_plate.model_dump())
    if aura_response == 400:
        return {"status": 400, "message": "Error creando la relacion"}
    else:
        return {"status": 200, "message": "Relacion creada exitosamente"}

# admin
@app.get("/admin/fill/location")
def fill_location():
    aura_response = aura.fill_locations()
    if aura_response == 400:
        return {"status": 400, "message": "Error llenando la locacion"}
    else:
        return {"status": 200, "message": "Locacion llenada exitosamente"}
    
@app.delete("/admin/delete/location")
def delete_location():
    aura_response = aura.delete_all_locations()
    if aura_response == 400:
        return {"status": 400, "message": "Error eliminando la locacion"}
    else:
        return {"status": 200, "message": "Locacion eliminada exitosamente"}

@app.put("/admin/birthday")
def birthdat(new_birthdate: str):
    aura_response = aura.update_user_birthday(new_birthdate)
    if aura_response == 400:
        return {"status": 400, "message": "Error actualizando la fecha de nacimiento"}
    else:
        return {"status": 200, "message": "Fecha de nacimiento actualizada exitosamente"}
    
@app.put("/admin/update_diner_birthday")
def update_diner_birthday(user_id: str, new_birthday: str):
    aura_response = aura.update_diner_birthday(new_birthday, user_id)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "message": "Diner birthday updated successfully"}

@app.put("/admin/add_diner_vegan")
def add_diner_vegan(user_id: str):
    aura_response = aura.add_diner_vegan(user_id)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "message": "Diner vegan property added successfully"}

@app.put("/admin/add_all_diners_vegan")
def add_all_diners_vegan():
    aura_response = aura.add_all_diners_vegan()
    return {"status": 200, "message": "All diners vegan property added successfully"}

@app.put("/admin/delete_diner_vegan")
def delete_diner_vegan(user_id: str):
    aura_response = aura.delete_diner_vegan(user_id)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "message": "Diner vegan property deleted successfully"}

@app.put("/admin/delete_all_diners_vegan")
def delete_all_diners_vegan():
    aura_response = aura.delete_all_diners_vegan()
    return {"status": 200, "message": "All diners vegan property deleted successfully"}

@app.put("/admin/update_ingredient_dish_cook_time")
def update_ingredient_dish_cook_time(ingredient_name: str, dish_name: str, new_cook_time: int):
    aura_response = aura.update_ingredient_dish_cook_time(ingredient_name, dish_name, new_cook_time)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="Ingredient or dish not found")
    return {"status": 200, "message": "Ingredient-dish cook time updated successfully"}

@app.put("/admin/update_dish_ingredients_cook_time")
def update_dish_ingredients_cook_time(dish_name: str, new_cook_time: int):
    aura_response = aura.update_dish_ingredients_cook_time(dish_name, new_cook_time)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="Dish not found")
    return {"status": 200, "message": "Dish ingredients cook time updated successfully"}

@app.put("/admin/add_ingredient_dish_cook_temperature")
def add_ingredient_dish_cook_temperature(ingredient_name: str, dish_name: str, cook_temperature: int):
    aura_response = aura.add_ingredient_dish_cook_temperature(ingredient_name, dish_name, cook_temperature)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="Ingredient or dish not found")
    return {"status": 200, "message": "Ingredient-dish cook temperature added successfully"}

@app.put("/admin/add_dish_ingredients_cook_temperature")
def add_dish_ingredients_cook_temperature(dish_name: str, cook_temperature: int):
    aura_response = aura.add_dish_ingredients_cook_temperature(dish_name, cook_temperature)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="Dish not found")
    return {"status": 200, "message": "Dish ingredients cook temperature added successfully"}

@app.put("/admin/delete_ingredient_dish_cook_temperature")
def delete_ingredient_dish_cook_temperature(ingredient_name: str, dish_name: str):
    aura_response = aura.delete_ingredient_dish_cook_temperature(ingredient_name, dish_name)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="Ingredient or dish not found")
    return {"status": 200, "message": "Ingredient-dish cook temperature deleted successfully"}

@app.put("/admin/delete_dish_ingredients_cook_temperature")
def delete_dish_ingredients_cook_temperature(dish_name: str):
    aura_response = aura.delete_dish_ingredients_cook_temperature(dish_name)
    if aura_response == 404:
        raise HTTPException(status_code=404, detail="Dish not found")
    return {"status": 200, "message": "Dish ingredients cook temperature deleted successfully"}
    
@app.get("/diner/recommend")
def recommend_dishes(user_id: str, limit: int):
    aura_response = sistema_recomendacion(user_id, limit)
    if aura_response == 404:
        return {"status": 404, "message": "El usuario no existe"}
    elif aura_response == 400:
        return {"status": 400, "message": "Error obteniendo las recomendaciones"}
    else:
        return {"status": 200, "message": "Recomendaciones creadas exitosamente", "data": aura_response}
    
@app.post("/admin/execute_query")
def execute_query(query: str):
    aura_response = aura.execute_query(query)
    if aura_response == 400:
        return {"status": 400, "message": "Error ejecutando la query"}
    else:
        return {"status": 200, "message": "Query ejecutada exitosamente", "data": aura_response}
    
# Para correrlo en local
if __name__ == "__main__":
    uvicorn.run(app, port=8000)