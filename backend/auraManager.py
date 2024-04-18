import csv
from datetime import datetime
import random
from neo4j import GraphDatabase, Transaction

link = "neo4j+s://9b98ec60.databases.neo4j.io"
user = "neo4j"
password ="lKN_EQiO6tvAV3x-hLlN3JZOtJMcdGktvq1QsDnBJbw"



class AuraNeo4j:
    driver: GraphDatabase

    def __init__(self, uri: str=link, user: str=user, password: str=password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def user_login(self, user_id: str, password: str):
        with self.driver.session() as session:
            return session.read_transaction(self._user_login, user_id, password)
        
    @staticmethod
    def _user_login(tx: Transaction, user_id: str, password: str):
        # buscar en el nodo Diner o Restaurant si el usuario y contraseña coinciden. Retornar el nombre del nodo como rol
        search_query = (
            "MATCH (c) WHERE c.user_id = $user_id AND c.password = $password "
            "RETURN labels(c)[0] AS role"
        )
        if tx.run(search_query, user_id=user_id, password=password).single() is not None:
            return tx.run(search_query, user_id=user_id, password=password).single()
        else:
            return 404
            
    
    def search_user(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_user, user_id)

    def create_diner(self, user: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_diner, user)

    @staticmethod
    def _create_diner(tx: Transaction, user: dict):
        search_query = "MATCH (c:Diner {user_id: $user_id}) RETURN c"
        result = tx.run(search_query, user_id=user['user_id']).single()
        if result is not None:
            return 409  # Un usuario con este ID ya existe

        create_query = (
            "MERGE (c:User:Diner {user_id: $user_id, password: $password, name: $name, "
            "lastname: $lastname, brithdate: $birthdate, spending: $spending, "
            "has_car: $has_car, image: $image}) "
            "RETURN c"
        )
        try:
            return tx.run(create_query, **user).single()[0]
        except Exception as e:
            return 400
        
    def create_restaurant(self, user: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_restaurant, user)
        
    @staticmethod
    def _create_restaurant(tx: Transaction, user: dict):
        search_query = "MATCH (c:Restaurant {user_id: $user_id}) RETURN c"
        result = tx.run(search_query, user_id=user['user_id']).single()
        if result is not None:
            return 409  # Un usuario con este ID ya existe

        create_query = (
            "MERGE (c:User:Restaurant {user_id: $user_id, password: $password, name: $name, "
            "prices: $prices, rating: -1, schedule: $schedule, "
            "sells_alcohol: $sells_alcohol, petFriendly: $petFriendly, imagen: $imagen}) "
            "RETURN c"
        )
        try:
            return tx.run(create_query, **user).single()[0]
        except Exception as e:
            return 400
    
    def create_location(self, location: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_location, location)
    
    @staticmethod
    def _create_location(tx: Transaction, location: dict):
        search_query = "MATCH (l:Location {country: $country, city: $city, zone: $zone, postal_code: $postal_code}) RETURN l"
        result = tx.run(search_query, country=location['country'], city=location['city'], zone=location['zone'], postal_code=location['postal_code']).single()
        if result is not None:
            return 409  # Una ubicación con estos detalles ya existe
    
        create_query = (
            "MERGE (l:Location {country: $country, city: $city, zone: $zone, "
            "is_dangerous: $is_dangerous, postal_code: $postal_code}) "
            "RETURN l"
        )
        try:
            return tx.run(create_query, **location).single()[0]
        except Exception as e:
            return 400
    
    def create_ingredient(self, ingredient: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_ingredient, ingredient)

    @staticmethod
    def _create_ingredient(tx: Transaction, ingredient: dict):
        search_query = "MATCH (i:Ingredient {name: $name}) RETURN i"
        result = tx.run(search_query, name=ingredient['name'], type=ingredient['type']).single()
        if result is not None:
            return 409  # Un ingrediente con estos detalles ya existe

        create_query = (
            "MERGE (i:Ingredient {name: $name, type: $type, calories: $calories, "
            "is_vegan: $is_vegan, has_gluten: $has_gluten}) "
            "RETURN i"
        )
        try:
            return tx.run(create_query, **ingredient).single()[0]
        except Exception as e:
            return 400

    def create_dish(self, dish: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_dish, dish)
        
    @staticmethod
    def _create_dish(tx: Transaction, dish: dict):
        search_query = "MATCH (d:Dish {name: $name}) RETURN d"
        result = tx.run(search_query, name=dish['name']).single()
        if result is not None:
            return 409  # Un plato con este nombre ya existe

        """
            name: str
            description: str
            is_vegan: bool
            avg_price: float
            has_alcohol: bool
        """
        create_query = (
            "MERGE (d:Dish {name: $name, description: $description, is_vegan: $is_vegan, "
            "avg_price: $avg_price, has_alcohol: $has_alcohol}) "
            "RETURN d"
        )

        try:
            return tx.run(create_query, **dish).single()[0]
        except Exception as e:
            return 400
        
    def create_parking(self, parking: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_parking, parking)
        
    @staticmethod
    def _create_parking(tx: Transaction, parking: dict):
        search_query = "MATCH (p:Parking {parking_id: $parking_id}) RETURN p"
        result = tx.run(search_query, parking_id=parking['parking_id']).single()
        if result is not None:
            return 409  # Un parqueadero con este ID ya existe

        create_query = (
            "MERGE (p:Parking {parking_id: $parking_id, price_per_hour: $price_per_hour, capacity: $capacity, handicap_friendly: $handicap_friendly, has_security: $has_security, is_covered: $is_covered}) RETURN p"
        )
        try:
            return tx.run(create_query, **parking).single()[0]
        except Exception as e:
            return 400
    
    def search_restaurant(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_restaurant, user_id)
        
    @staticmethod
    def _search_restaurant(tx: Transaction, user_id: str):
        search_query = "MATCH (c:Restaurant {user_id: $user_id}) RETURN c"
        try:
            return tx.run(search_query, user_id=user_id).single()
        except Exception as e:
            return 404
        
    def search_ingredient(self, name: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_ingredient, name)
        
    @staticmethod
    def _search_ingredient(tx: Transaction, name: str):
        search_query = "MATCH (i:Ingredient {name: $name}) RETURN i"
        try:
            return tx.run(search_query, name=name).single()
        except Exception as e:
            return 404 # No se encontró el ingrediente
        
    def search_dish(self, name: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_dish, name)
        
    @staticmethod
    def _search_dish(tx: Transaction, name: str):
        search_query = "MATCH (d:Dish {name: $name}) RETURN d"
        try:
            return tx.run(search_query, name=name).single()
        except Exception as e:
            return 404 # No se encontró el plato
        
    def search_location(self, city: str, zone: int):
        with self.driver.session() as session:
            return session.read_transaction(self._search_location, city, zone)
        
    @staticmethod
    def _search_location(tx: Transaction, city: str, zone: int):
        search_query = "MATCH (l:Location {city: $city, zone: $zone}) RETURN l"
        try:
            return tx.run(search_query, city=city, zone=zone).single()
        except Exception as e:
            return 404 # No se encontró la ubicación
        
    def search_parking(self, parking_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_parking, parking_id)
        
    @staticmethod
    def _search_parking(tx: Transaction, parking_id: str):
        search_query = "MATCH (p:Parking {parking_id: $parking_id}) RETURN p"
        try:
            return tx.run(search_query, parking_id=parking_id).single()
        except Exception as e:
            return 404 # No se encontró el parqueadero
        


    # Crear relacion entre usuario y restaurante llamada visitó con propiedades: dishes, total, date, rating, comment
    def create_visit(self, visit: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_visit, visit)
        
    @staticmethod
    def _create_visit(tx: Transaction, visit: dict):
        create_visit_query = (
            "MATCH (u:Diner {user_id: $user_id}), (c:Restaurant {user_id: $restaurant_id}) "
            "MERGE (u)-[r:VISITED {dishes: $dishes, total: $total, date: $date, rating: $rating, comment: $comment}]->(c) "
            "RETURN r"
        )
        try:
            result = tx.run(create_visit_query, **visit).single()

            # Actualizar el rating del restaurante
            update_rating_query = (
                "MATCH (c:Restaurant {user_id: $restaurant_id})<-[r:VISITED]-(:Diner) "
                "WITH c, AVG(r.rating) AS new_rating "
                "SET c.rating = new_rating "
                "RETURN c.rating"
            )
            tx.run(update_rating_query, restaurant_id=visit['restaurant_id'])

            return result[0]
        except Exception as e:
            return 400
        
        # crear la relacion entre diner y location llamada lives_in con las propiedades street, avenue, number, community, reference. el id de la locacion es la zone
    def diner_lives_in(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._diner_lives_in, relationship)
        
    @staticmethod
    def _diner_lives_in(tx: Transaction, relationship: dict):
        search_query = (
            "MATCH (d:Diner {user_id: $diner_id}), (l:Location {zone: $zone}) "
            "MERGE (d)-[li:LIVES_IN {street: $street, avenue: $avenue, number: $number, community: $community, reference: $reference}]->(l) "
            "RETURN li"
        )
        try:
            return tx.run(search_query, **relationship).single()[0]
        except Exception as e:
            return 400
        
    # Crear relacion entre restaurante y location llamada located_in con propiedades: street, avenue, number, community, reference
    def restaurant_located_in(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._restaurant_located_in, relationship)
        
    @staticmethod
    def _restaurant_located_in(tx: Transaction, relationship: dict):
        check_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[li:LOCATED_IN]->(l:Location) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **relationship).single()
            if result["count"] > 0:
                return 200  # O cualquier otro código de estado que desees
            else:
                create_query = (
                    "MATCH (r:Restaurant {user_id: $restaurant_id}), (l:Location {zone: $zone}) "
                    "MERGE (r)-[li:LOCATED_IN {street: $street, avenue: $avenue, number: $number, community: $community, reference: $reference}]->(l) "
                    "RETURN li"
                )
                return tx.run(create_query, **relationship).single()[0]
        except Exception as e:
            return 400
        
    
    def serach_restaurant_location(self, restaurant_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._serach_restaurant_location, restaurant_id)
        
    @staticmethod
    def _serach_restaurant_location(tx: Transaction, restaurant_id: str):
        search_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[li:LOCATED_IN]->(l:Location) "
            "RETURN li"
        )
        try:
            response = tx.run(search_query, restaurant_id=restaurant_id).single()
            if response is not None:
                return response[0]
            else:
                return 404
        except Exception as e:
            return 400

    def search_restaurant_zone(self, restaurant_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_restaurant_zone, restaurant_id)
        
    @staticmethod
    def _search_restaurant_zone(tx: Transaction, restaurant_id: str):
        search_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[li:LOCATED_IN]->(l:Location) "
            "RETURN l.zone AS zone"
        )
        try:
            response = tx.run(search_query, restaurant_id=restaurant_id).single()
            if response is not None:
                return response[0]
            else:
                return 404
        except Exception as e:
            return 400
        
    def search_sells_relationship(self, restaurant_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_sells_relationship, restaurant_id)

    @staticmethod
    def _search_sells_relationship(tx: Transaction, restaurant_id: str):
        search_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[s:SELLS]->(d:Dish) "
            "RETURN d"
        )
        try:
            response = tx.run(search_query, restaurant_id=restaurant_id)
            return [record[0] for record in response]
        except Exception as e:
            return 404

    
    
    def diner_on_restaurant(self, diner_on_restaurnt:dict): # debería recibir del basemodel diner_on_restaurant. 
        with self.driver.session() as session:
            return session.write_transaction(self._diner_on_restaurant, diner_on_restaurnt)
        
    @staticmethod
    def _diner_on_restaurant(tx: Transaction, diner_on_restaurnt: dict):
        """
        diner on restaurant
            diner_id: str
            restaurant_id: str
            its_fav: bool
            user_likes: bool
            comments: str
        relation should be named diner_on_restaurnt
        """

        check_query = (
            "MATCH (d:Diner {user_id: $diner_id})-[do:DINER_ON_RESTAURANT]->(r:Restaurant {user_id: $restaurant_id}) "
            "RETURN COUNT(*) AS count"
        )

        try:
            result = tx.run(check_query, **diner_on_restaurnt).single()
            if result["count"] > 0:
                return 200  # O cualquier otro código de estado que desees
            else:
                create_query = (
                    "MATCH (d:Diner {user_id: $diner_id}), (r:Restaurant {user_id: $restaurant_id}) "
                    "MERGE (d)-[do:DINER_ON_RESTAURANT {its_fav: $its_fav, user_likes: $user_likes, comments: $comments}]->(r) "
                    "RETURN do"
                )
                return tx.run(create_query, **diner_on_restaurnt).single()[0]
        except Exception as e:
            return 400


    # Crear relacion entre restaurante y plato llamada sells con propiedades: price, sell_time and cost
    def restaurant_sells(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._restaurant_sells, relationship)
            
    @staticmethod
    def _restaurant_sells(tx: Transaction, relationship: dict):
        # Primera consulta: Buscar si la relación ya existe
        check_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[s:SELLS]->(d:Dish {name: $dish_id}) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **relationship).single()
            if result["count"] > 0:
                # La relación ya existe, no es necesario crearla
                return 200  # O cualquier otro código de estado que desees
            else:
                    # Segunda consulta: Crear la relación si no existe
                create_query = (
                    "MATCH (r:Restaurant {user_id: $restaurant_id}), (d:Dish {name: $dish_id}) "
                    "MERGE (r)-[s:SELLS {price: $price, sell_time: $sell_time, cost: $cost}]->(d) "
                    "RETURN s"
                )
                try:
                    return tx.run(create_query, **relationship).single()[0]
                except Exception as e:
                    return 400
        except Exception as e:
            return 400


        
    def get_all_location_zones(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_all_location_zones)

    @staticmethod
    def _get_all_location_zones(tx: Transaction):
        search_query = (
            "MATCH (l:Location) "
            "RETURN DISTINCT l.zone AS zone "
            "ORDER BY zone ASC"
        )
        try:
            result = tx.run(search_query)
            return [record["zone"] for record in result]
        except Exception as e:
            return None
        
    def get_all_ingredients(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_all_ingredients)
        
    @staticmethod
    def _get_all_ingredients(tx: Transaction):
        search_query = (
            "MATCH (i:Ingredient) "
            "RETURN i.name AS name"
        )
        try:
            result = tx.run(search_query)
            return [record["name"] for record in result]
        except Exception as e:
            return None
        
    def get_all_dishes(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_all_dishes)
        
    @staticmethod
    def _get_all_dishes(tx: Transaction):
        search_query = (
            "MATCH (d:Dish) "
            "RETURN d.name AS name"
        )
        try:
            result = tx.run(search_query)
            return [record["name"] for record in result]
        except Exception as e:
            return None
        
    def get_all_restaurants(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_all_restaurants)
        
    @staticmethod
    def _get_all_restaurants(tx: Transaction):
        search_query = (
            "MATCH (r:Restaurant) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(search_query)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    def get_all_diners(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_all_diners)
        
    @staticmethod
    def _get_all_diners(tx: Transaction):
        search_query = (
            "MATCH (d:Diner) "
            "RETURN d.user_id AS user_id"
        )
        try:
            result = tx.run(search_query)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
    # Crear relacion entre diner y platillo llamada dish_opinion con propiedades: favorite, likes, comment
    def diner_opinion(self, opinion: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._diner_opinion, opinion)
        
    @staticmethod
    def _diner_opinion(tx: Transaction, opinion: dict):
        check_query = (
            "MATCH (d:Diner {user_id: $diner_id})-[do:DISH_OPINION]->(di:Dish {name: $dish_id}) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **opinion).single()
            if result["count"] > 0:
                return 200  # O cualquier otro código de estado que desees
            else:
                create_query = (
                    "MATCH (d:Diner {user_id: $diner_id}), (di:Dish {name: $dish_id}) "
                    "MERGE (d)-[do:DISH_OPINION {favorite: $favorite, likes: $likes, comment: $comment}]->(di) "
                    "RETURN do"
                )
                return tx.run(create_query, **opinion).single()[0]
        except Exception as e:
            return 400

    # Crear relacion entre restaurante y parqueadero llamada has_parking con propiedades: vallet parking, free_hours, exclusive
    def restaurant_has_parking(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._restaurant_has_parking, relationship)
        
    @staticmethod
    def _restaurant_has_parking(tx: Transaction, relationship: dict):
        check_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[hp:HAS_PARKING]->(p:Parking) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **relationship).single()
            if result["count"] > 0:
                return 200  # O cualquier otro código de estado que desees
            else:
                create_query = (
                    "MATCH (r:Restaurant {user_id: $restaurant_id}), (p:Parking {parking_id: $parking_id}) "
                    "MERGE (r)-[hp:HAS_PARKING {vallet_parking: $vallet_parking, free_hours: $free_hours, exclusive: $exclusive}]->(p) "
                    "RETURN hp"
                )
                return tx.run(create_query, **relationship).single()[0]
        except Exception as e:
            return 400
        
    # relacion entre parqueo y ubicacion llamada parking_in con propiedades: street, avenue, number, community, reference
    def parking_in(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._parking_in, relationship)
        
    @staticmethod
    def _parking_in(tx: Transaction, relationship: dict):
        check_query = (
            "MATCH (p:Parking {parking_id: $parking_id})-[pi:PARKING_IN]->(l:Location) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **relationship).single()
            if result["count"] > 0:
                return 200  # O cualquier otro código de estado que desees
            else:
                create_query = (
                    "MATCH (p:Parking {parking_id: $parking_id}), (l:Location {zone: $zone}) "
                    "MERGE (p)-[pi:PARKING_IN {street: $street, avenue: $avenue, number: $number, community: $community, reference: $reference}]->(l) "
                    "RETURN pi"
                )
                return tx.run(create_query, **relationship).single()[0]
        except Exception as e:
            return 400
        
    def get_parking_location(self, parking_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_parking_location, parking_id)
        
    @staticmethod
    def _get_parking_location(tx: Transaction, parking_id: str):
        search_query = (
            "MATCH (p:Parking {parking_id: $parking_id})-[pi:PARKING_IN]->(l:Location) "
            "RETURN l"
        )
        try:
            return tx.run(search_query, parking_id=parking_id).single()[0]
        except Exception as e:
            return 404

    def get_all_parkings(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_all_parkings)
        
    @staticmethod
    def _get_all_parkings(tx: Transaction):
        search_query = (
            "MATCH (p:Parking) "
            "RETURN p.parking_id AS parking_id"
        )
        try:
            result = tx.run(search_query)
            return [record["parking_id"] for record in result]
        except Exception as e:
            return None
        
    # crear relacion entre restaurante y location llamada has_delivery con propiedades: price, time, own_delivery
    def restaurant_has_delivery(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._restaurant_has_delivery, relationship)   
        
    @staticmethod
    def _restaurant_has_delivery(tx: Transaction, relationship: dict):
        check_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[hd:HAS_DELIVERY]->(l:Location {zone: $zone}) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **relationship).single()
            if result["count"] > 0:
                return 200  # O cualquier otro código de estado que desees
            else:
                create_query = (
                    "MATCH (r:Restaurant {user_id: $restaurant_id}), (l:Location {zone: $zone}) "
                    "MERGE (r)-[hd:HAS_DELIVERY {price: $price, time: $time, own_delivery: $own_delivery}]->(l) "
                    "RETURN hd"
                )
                return tx.run(create_query, **relationship).single()[0]
        except Exception as e:
            return 400
        
        
    def get_user_info(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_user_info, user_id)
        
    @staticmethod
    def _get_user_info(tx: Transaction, user_id: str):
        search_query = (
            "MATCH (u) WHERE u.user_id = $user_id "
            "RETURN u"
        )
        try:
            return tx.run(search_query, user_id=user_id).single()[0]
        except Exception as e:
            return 404
        
    def update_user_info(self, user_id: str, new_info: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._update_user_info, user_id, new_info)
        
    @staticmethod
    def _update_user_info(tx: Transaction, user_id: str, new_info: dict):
        search_query = (
            "MATCH (u) WHERE u.user_id = $user_id "
            "SET u += $new_info "
            "RETURN u"
        )
        try:
            return tx.run(search_query, user_id=user_id, new_info=new_info).single()[0]
        except Exception as e:
            return 404
        
    def delete_user(self, user_id: str):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_user, user_id)
        
    @staticmethod
    def _delete_user(tx: Transaction, user_id: str):
        search_query = (
            "MATCH (u) WHERE u.user_id = $user_id "
            "DETACH DELETE u"
        )
        try:
            tx.run(search_query, user_id=user_id)
            return 200
        except Exception as e:
            return 404
        
    # crear relacion entre ingrediente y plato llamada has_ingredient con propiedades: quantity, cook_method, cook_time
    def dish_has_ingredient(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._dish_has_ingredient, relationship)
        
    @staticmethod
    def _dish_has_ingredient(tx: Transaction, relationship: dict):
        # Primera consulta: Buscar si la relación ya existe
        check_query = (
            "MATCH (d:Dish {name: $dish_id})<-[:USED_IN]-(i:Ingredient {name: $ingredient_id}) "
            "RETURN COUNT(*) AS count"
        )
        try:
            result = tx.run(check_query, **relationship).single()
            if result["count"] > 0:
                # La relación ya existe, no es necesario crearla
                return 200  # O cualquier otro código de estado que desees
            else:
                 # Segunda consulta: Crear la relación si no existe
                create_query = (
                    "MATCH (d:Dish {name: $dish_id}), (i:Ingredient {name: $ingredient_id}) "
                    "CREATE (i)-[hi:USED_IN {quantity: $quantity, cook_method: $cook_method, cook_time: $cook_time}]->(d) "
                    "RETURN hi"
                )
                try:
                    tx.run(create_query, **relationship)
                    return 201  # O cualquier otro código de estado que desees para indicar que se creó la relación
                except Exception as e:
                    return 400
        except Exception as e:
            return 400


    def delete_diner_visit(self, user_id: str, restaurant_id: str):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_diner_visit, user_id, restaurant_id)
        
    @staticmethod
    def _delete_diner_visit(tx: Transaction, user_id: str, restaurant_id: str):
        search_query = (
            "MATCH (d:Diner {user_id: $user_id})-[v:VISITED]->(r:Restaurant {user_id: $restaurant_id}) "
            "DELETE v"
        )
        try:
            tx.run(search_query, user_id=user_id, restaurant_id=restaurant_id)
            return 200
        except Exception as e:
            return 404
        
    def fill_locations(self):
        with self.driver.session() as session:
            return session.write_transaction(self._fill_locations)
        
    @staticmethod
    def _fill_locations(tx: Transaction):
        # Crear ubicaciones con zonas de 1 a 25 en guatemala sin el 20, 22 y 23. 1 por zona. el postal_code es la 10 conctatenado con zona
        create_query = (
            "UNWIND range(1, 25) AS zone "
            "WITH zone, CASE WHEN zone > 19 THEN zone + 2 ELSE zone END AS new_zone "
            "MERGE (l:Location {country: 'Guatemala', city: 'Guatemala', zone: new_zone, is_dangerous: false, postal_code: toInteger('10' + toString(new_zone))}) "
            "RETURN l"
        )
        try:
            return tx.run(create_query)
        except Exception as e:
            return 400
        
    def delete_all_locations(self):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_all_locations)
        
    @staticmethod
    def _delete_all_locations(tx: Transaction):
        search_query = (
            "MATCH (l:Location) "
            "DETACH DELETE l"
        )
        try:
            tx.run(search_query)
            return 200
        except Exception as e:
            return 404
        
    #actualizar la propiedad birthday de un usuario para convertirlo en date y no string YYYY-MM-DD
    def update_user_birthday(self, new_birthday: str):
        with self.driver.session() as session:
            return session.write_transaction(self._update_user_birthday, new_birthday)
        
    @staticmethod
    def _update_user_birthday(tx: Transaction, new_birthday: str):
        search_query = (
            "MATCH (d:Diner) "
            "SET d.birthday = date($new_birthday) "
            "REMOVE d.brithdate "
            "RETURN d"
        )
        try:
            # Remove brithdate and birthday properties from Restaurant
            remove_restaurant_properties_query = (
                "MATCH (r:Restaurant) "
                "REMOVE r.brithdate, r.birthday"
            )
            tx.run(remove_restaurant_properties_query)
            return tx.run(search_query, new_birthday=new_birthday).single()[0]
        except Exception as e:
            return 404
        
    #actualizar la propiedad birthday de un usuario para convertirlo en date y no string YYYY-MM-DD
    def update_diner_birthday(self, new_birthday: str, user_id: str):
        with self.driver.session() as session:
            return session.write_transaction(self._update_diner_birthday, new_birthday, user_id)
        
    @staticmethod
    def _update_diner_birthday(tx: Transaction, new_birthday: str, user_id: str):
        search_query = (
            "MATCH (d:Diner {user_id: $user_id}) "
            "SET d.birthday = date($new_birthday) "
            "RETURN d"
        )
        try:
            return tx.run(search_query, new_birthday=new_birthday, user_id=user_id).single()[0]
        except Exception as e:
            return 404

    # agregar la propiedad vegan al nodo diner
    def add_diner_vegan(self, user_id: str):
        with self.driver.session() as session:
            return session.write_transaction(self._add_diner_vegan, user_id)
        
    @staticmethod
    def _add_diner_vegan(tx: Transaction, user_id: str):
        search_query = (
            "MATCH (d:Diner {user_id: $user_id}) "
            "SET d.vegan = true "
            "RETURN d"
        )
        try:
            return tx.run(search_query, user_id=user_id).single()[0]
        except Exception as e:
            return 404
        
    # agregar la propiedad vegan a todos los diner
    def add_all_diners_vegan(self):
        with self.driver.session() as session:
            return session.write_transaction(self._add_all_diners_vegan)
        
    @staticmethod
    def _add_all_diners_vegan(tx: Transaction):
        search_query = (
            "MATCH (d:Diner) "
            "SET d.vegan = false "
            "RETURN d"
        )
        try:
            return tx.run(search_query)
        except Exception as e:
            return 404
        

    # eliminar la propiedad vegan del nodo diner
    def delete_diner_vegan(self, user_id: str):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_diner_vegan, user_id)
        
    @staticmethod
    def _delete_diner_vegan(tx: Transaction, user_id: str):
        search_query = (
            "MATCH (d:Diner {user_id: $user_id}) "
            "REMOVE d.vegan "
            "RETURN d"
        )
        try:
            return tx.run(search_query, user_id=user_id).single()[0]
        except Exception as e:
            return 404
        
    # eliminar la propiedad vegan de todos los diner
    def delete_all_diners_vegan(self):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_all_diners_vegan)
        
    @staticmethod
    def _delete_all_diners_vegan(tx: Transaction):
        search_query = (
            "MATCH (d:Diner) "
            "REMOVE d.vegan "
            "RETURN d"
        )
        try:
            return tx.run(search_query)
        except Exception as e:
            return 404

    # actualizar la propiedad cook_time de la relacion entre ingrediente y plato
    def update_ingredient_dish_cook_time(self, ingredient_name: str, dish_name: str, new_cook_time: int):
        with self.driver.session() as session:
            return session.write_transaction(self._update_ingredient_dish_cook_time, ingredient_name, dish_name, new_cook_time)
        
    @staticmethod
    def _update_ingredient_dish_cook_time(tx: Transaction, ingredient_name: str, dish_name: str, new_cook_time: int):
        search_query = (
            "MATCH (i:Ingredient {name: $ingredient_name})-[hi:USED_IN]->(d:Dish {name: $dish_name}) "
            "SET hi.cook_time = $new_cook_time "
            "RETURN hi"
        )
        try:
            return tx.run(search_query, ingredient_name=ingredient_name, dish_name=dish_name, new_cook_time=new_cook_time).single()[0]
        except Exception as e:
            return 404
        
    # actualizar la propiedad cook_time para todos los ingredientes de un plato
    def update_dish_ingredients_cook_time(self, dish_name: str, new_cook_time: int):
        with self.driver.session() as session:
            return session.write_transaction(self._update_dish_ingredients_cook_time, dish_name, new_cook_time)
        
    @staticmethod
    def _update_dish_ingredients_cook_time(tx: Transaction, dish_name: str, new_cook_time: int):
        search_query = (
            "MATCH (d:Dish {name: $dish_name})<-[hi:USED_IN]-(i:Ingredient) "
            "SET hi.cook_time = $new_cook_time "
            "RETURN hi"
        )
        try:
            return tx.run(search_query, dish_name=dish_name, new_cook_time=new_cook_time)
        except Exception as e:
            return 404
        
    # agregar la propiedad cook_temperature a la relacion entre ingrediente y plato
    def add_ingredient_dish_cook_temperature(self, ingredient_name: str, dish_name: str, cook_temperature: int):
        with self.driver.session() as session:
            return session.write_transaction(self._add_ingredient_dish_cook_temperature, ingredient_name, dish_name, cook_temperature)
        
    @staticmethod
    def _add_ingredient_dish_cook_temperature(tx: Transaction, ingredient_name: str, dish_name: str, cook_temperature: int):
        search_query = (
            "MATCH (i:Ingredient {name: $ingredient_name})-[hi:USED_IN]->(d:Dish {name: $dish_name}) "
            "SET hi.cook_temperature = $cook_temperature "
            "RETURN hi"
        )
        try:
            return tx.run(search_query, ingredient_name=ingredient_name, dish_name=dish_name, cook_temperature=cook_temperature).single()[0]
        except Exception as e:
            return 404
        
    # agregar la propiedad cook_temperature a todas las relaciones entre ingredientes y platos
    def add_dish_ingredients_cook_temperature(self, dish_name: str, cook_temperature: int):
        with self.driver.session() as session:
            return session.write_transaction(self._add_dish_ingredients_cook_temperature, dish_name, cook_temperature)
        
    @staticmethod
    def _add_dish_ingredients_cook_temperature(tx: Transaction, dish_name: str, cook_temperature: int):
        search_query = (
            "MATCH (d:Dish {name: $dish_name})<-[hi:USED_IN]-(i:Ingredient) "
            "SET hi.cook_temperature = $cook_temperature "
            "RETURN hi"
        )
        try:
            return tx.run(search_query, dish_name=dish_name, cook_temperature=cook_temperature)
        except Exception as e:
            return 404
        

    # eliminar la propiedad cook_temperature de la relacion entre ingrediente y plato
    def delete_ingredient_dish_cook_temperature(self, ingredient_name: str, dish_name: str):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_ingredient_dish_cook_temperature, ingredient_name, dish_name)
        
    @staticmethod
    def _delete_ingredient_dish_cook_temperature(tx: Transaction, ingredient_name: str, dish_name: str):
        search_query = (
            "MATCH (i:Ingredient {name: $ingredient_name})-[hi:USED_IN]->(d:Dish {name: $dish_name}) "
            "REMOVE hi.cook_temperature "
            "RETURN hi"
        )
        try:
            return tx.run(search_query, ingredient_name=ingredient_name, dish_name=dish_name).single()[0]
        except Exception as e:
            return 404
        
    # eliminar la propiedad cook_temperature de todas las relaciones entre ingredientes y platos
    def delete_dish_ingredients_cook_temperature(self, dish_name: str):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_dish_ingredients_cook_temperature, dish_name)
        
    @staticmethod
    def _delete_dish_ingredients_cook_temperature(tx: Transaction, dish_name: str):
        search_query = (
            "MATCH (d:Dish {name: $dish_name})<-[hi:USED_IN]-(i:Ingredient) "
            "REMOVE hi.cook_temperature "
            "RETURN hi"
        )
        try:
            return tx.run(search_query, dish_name=dish_name)
        except Exception as e:
            return 404

    def get_ingredients(self, dish_name: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_ingredients, dish_name)
        
    @staticmethod
    def _get_ingredients(tx: Transaction, dish_name: str):
        search_query = (
            "MATCH (d:Dish {name: $dish_name})<-[hi:USED_IN]-(i:Ingredient) "
            "RETURN i.name AS name"
        )
        try:
            result = tx.run(search_query, dish_name=dish_name)
            return [record["name"] for record in result]
        except Exception as e:
            return None
        
    # obtener la resena de un usuario a un restaurante (visita) donde retorna el nombre del usuario, apellido y todas las propiedades de la relacion de visited
    def get_restaurant_reviews(self, restaurant_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_restaurant_reviews, restaurant_id)
        
    @staticmethod
    def _get_restaurant_reviews(tx: Transaction, restaurant_id: str):
        search_query = (
            "MATCH (d:Diner)-[v:VISITED]->(r:Restaurant {user_id: $restaurant_id}) "
            "RETURN  d.name as name, d.lastname as lastname, toString(v.date) as date, v.total as total, v.rating as rating, v.dishes as dishes, v.comment as comment"
        )
        try:
            result = tx.run(search_query, restaurant_id=restaurant_id)
            records = []
            for record in result:
                # Obtener los nombres de los campos
                keys = record.keys()
                # Mapear los valores con los nombres de los campos
                mapped_record = {key: record[key] for key in keys}
                records.append(mapped_record)
            return records
        except Exception as e:
            return None

    # obtener los restaurantes que le gustan al usuario (rating > 3)
    def get_user_likes(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_user_likes, user_id)
        
    @staticmethod
    def _get_user_likes(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[v:VISITED]->(r:Restaurant) "
            "WHERE v.rating > 3 "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
    
    # obtener los restaurantes que estan en la misma zona que el usuario
    def get_zone_restaurants(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_zone_restaurants, user_id)
        
    @staticmethod
    def _get_zone_restaurants(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[li:LIVES_IN]->(l:Location) "
            "MATCH (r:Restaurant)-[li:LOCATED_IN]->(l) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # obtener los restaurantes que tienen los platos favoritos del usuario
    def get_fav_dishes_restaurants(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_fav_dishes_restaurants, user_id)
        
    @staticmethod
    def _get_fav_dishes_restaurants(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[do:DISH_OPINION {favorite: true}]->(di:Dish) "
            "MATCH (r:Restaurant)-[s:SELLS]->(di) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # obtener los restaurantes que tienen los platos que le gustan al usuario
    def get_likes_dishes_restaurants(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_likes_dishes_restaurants, user_id)
        
    @staticmethod
    def _get_likes_dishes_restaurants(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[do:DISH_OPINION {likes: true}]->(di:Dish) "
            "MATCH (r:Restaurant)-[s:SELLS]->(di) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # si el usuario tiene carro, obtener los restaurantes que tienen parqueo
    def get_car_parking_restaurants(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_car_parking_restaurants, user_id)
        
    @staticmethod
    def _get_car_parking_restaurants(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id}) "
            "WHERE d.has_car = true "
            "MATCH (r:Restaurant)-[hp:HAS_PARKING]->(p:Parking) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # obtener los restaurantes que tienen delivery a la zona del usuario
    def get_delivery_restaurants(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_delivery_restaurants, user_id)
        
    @staticmethod
    def _get_delivery_restaurants(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[li:LIVES_IN]->(l:Location) "
            "MATCH (r:Restaurant)-[hd:HAS_DELIVERY]->(l) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # obtener los restaurantes que tienen un rating mayor a 4
    def get_rating_restaurants(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_rating_restaurants, user_id)
        
    @staticmethod
    def _get_rating_restaurants(tx: Transaction, user_id: str):
        query = (
            "MATCH (r:Restaurant) "
            "WHERE r.rating > 4 "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # obtener los restaurantes que le gusta al usuario
    def get_user_likes_restaurant(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_user_likes_restaurant, user_id)
        
    @staticmethod
    def _get_user_likes_restaurant(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[do:DINER_ON_RESTAURANT {user_likes: true}]->(r:Restaurant) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    # obtener los restaurantes que son los favoritos del usuario
    def get_user_favs(self, user_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_user_favs, user_id)
        
    @staticmethod
    def _get_user_favs(tx: Transaction, user_id: str):
        query = (
            "MATCH (d:Diner {user_id: $user_id})-[do:DINER_ON_RESTAURANT {its_fav: true}]->(r:Restaurant) "
            "RETURN r.user_id AS user_id"
        )
        try:
            result = tx.run(query, user_id=user_id)
            return [record["user_id"] for record in result]
        except Exception as e:
            return None
        
    #metodo para ejecutar un query
    def run_query(self, query: str):
        with self.driver.session() as session:
            return session.read_transaction(self._run_query, query)
    
    @staticmethod
    def _run_query(tx: Transaction, query: str):
        try:
            response = tx.run(query)
            return 200, [record for record in response]
        except Exception as e:
            return 400, e

    def load_dishes_from_csv(self, file_path: str):
        # Abrir el archivo CSV y leer los datos
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Construir la consulta para insertar cada fila en Neo4j
                query = """
                MERGE (d:Dish {name: $name, description: $description, is_vegan: $is_vegan, 
                avg_price: $avg_price, has_alcohol: $has_alcohol}) 
                RETURN d
                """
                # Ejecutar la consulta para insertar la fila actual en Neo4j
                with self.driver.session() as session:
                    session.write_transaction(self._run_query_csv, query, **row)

        return 200
    
    def load_parking_from_csv(self, file_path: str):
        # Abrir el archivo CSV y leer los datos
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Construir la consulta para insertar cada fila en Neo4j
                #parking_id: $parking_id, price_per_hour: $price_per_hour, capacity: $capacity, handicap_friendly: $handicap_friendly, has_security: $has_security, is_covered: $is_covered
                query = """
                MERGE (p:Parking {parking_id: $parking_id, price_per_hour: toFloat($price_per_hour), capacity: toInteger($capacity),
                handicap_friendly: toBoolean($handicap_friendly), has_security: toBoolean($has_security), is_covered: toBoolean($is_covered)})
                RETURN p
                """
                # Ejecutar la consulta para insertar la fila actual en Neo4j
                with self.driver.session() as session:
                    session.write_transaction(self._run_query_csv, query, **row)

        return 200

    def load_ingredients_from_csv(self, file_path: str):
        # Abrir el archivo CSV y leer los datos
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Construir la consulta para insertar cada fila en Neo4j
                query = """
                MERGE (i:Ingredient {name: $name, type: $type, calories: toInteger($calories), 
                is_vegan: toBoolean($is_vegan), has_gluten: toBoolean($has_gluten)})
                """
                # Ejecutar la consulta para insertar la fila actual en Neo4j
                with self.driver.session() as session:
                    session.write_transaction(self._run_query_csv, query, **row)

        return 200

    # Método _run_query_csv actualizado para tomar parámetros adicionales
    @staticmethod
    def _run_query_csv(tx: Transaction, query: str, **row):
        try:
            tx.run(query, **row)
            return 200
        except Exception as e:
            return 400


        
        
        
        
def sistema_recomendacion(user_id: str, limit: int = 20):
    aura = AuraNeo4j()

    # verificar si el usuario existe
    user = aura.get_user_info(user_id)
    if user == 404:
        return 404

    try:
        # obtener los restaurantes que le gustan al usuario (rating > 3)

        likes_restaurants = aura.get_user_likes(user_id)


        # obtener los restaurantes que estan en la misma zona que el usuario

        zone_restaurants = aura.get_zone_restaurants(user_id)

        # obtener los restaurantes que tienen los platos favoritos del usuario
        
        fav_dishes_restaurants = aura.get_fav_dishes_restaurants(user_id)

        # obtener los restaurantes que tienen los platos que le gustan al usuario

        likes_dishes_restaurants = aura.get_likes_dishes_restaurants(user_id)

        # si el usuario tiene carro, obtener los restaurantes que tienen parqueo

        car_parking_restaurants = aura.get_car_parking_restaurants(user_id)

        # obtener los restaurantes que tienen delivery a la zona del usuario

        delivery_restaurants = aura.get_delivery_restaurants(user_id)

        # obtener los restaurantes que tienen un rating mayor a 4

        rating_restaurants = aura.get_rating_restaurants(user_id)

        # obtener los restaurantes que le gusta al usuario

        user_likes = aura.get_user_likes_restaurant(user_id)

        # obtener los restaurantes que son los favoritos del usuario

        user_favs = aura.get_user_favs(user_id)

        # combinar todas las recomendaciones. Se puede hacer un conteo de cuantas veces aparece cada restaurante en las recomendaciones y ordenarlos de mayor a menor
        recommendations = likes_restaurants + zone_restaurants + fav_dishes_restaurants + likes_dishes_restaurants + car_parking_restaurants + delivery_restaurants + rating_restaurants + user_likes + user_favs
        recommendations = {restaurant: recommendations.count(restaurant) for restaurant in recommendations}
        recommendations = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))
        
        # tomar las primeras 20 recomendaciones
        recommendations = list(recommendations.keys())[:limit]

        # obtener la informacion de los restaurantes recomendados
        recommended_restaurants = []
        for restaurant_id in recommendations:
            restaurant = aura.get_user_info(restaurant_id)
            location = aura.search_restaurant_zone(restaurant_id)  
            restaurant = dict(restaurant) 
            if location == 404:
                location = ""
                restaurant['location'] = location
            else:
                restaurant['location'] = location
            recommended_restaurants.append(restaurant)

        return recommended_restaurants
    except Exception as e:
        return 400
    
# funcion para meter muchos datos a la base de datos
def fill_db_ingredients():
    aura = AuraNeo4j()
    # crear 500 ingredientes con datos random  y los name deben ser unicos
    #array de ingredientes
    ingredients = ["Quinoa", "Lentejas", "Tofu", "Tempeh", "Hummus", "Kale", "Algas marinas", "Champiñones", "Berenjena", "Remolacha", "Col rizada", "Cúrcuma", "Jengibre", "Ajo", "Cebolla morada", "Rúcula", "Rabanitos", "Zapallo", "Chía", "Linaza", "Almendras", "Nueces", "Piñones", "Cacahuetes", "Anacardos", "Avellanas", "Macadamias", "Pistachos", "Almendras", "Mantequilla de almendras", "Mantequilla de cacahuetes", "Mantequilla de nueces", "Mantequilla de anacardos", "Mantequilla de avellanas", "Mantequilla de coco", "Mantequilla de girasol", "Mantequilla de sésamo", "Mantequilla de castañas de cajú", "Mantequilla de nueces de macadamia", "Mantequilla de pistachos"]
    # crear con las propiedades: name, calories, type, has_gluten, is_vegan
    for ingredient in ingredients:
        ingredient = {
            "name": ingredient,
            "calories": random.randint(1, 1000),
            "type": random.choice(["vegetable", "fruit", "meat", "dairy", "grain", "drink", "alcohol", "sweet", "spice", "condiment"]),
            "has_gluten": random.choice([True, False]),
            "is_vegan": random.choice([True, False])
        }
        aura.create_ingredient(ingredient)

def fill_db_dishes():
    aura = AuraNeo4j()
    # crear 1000 platos con datos random y los name deben ser unicos
    #array de platos
    dishes = ["Tacos", "Enchiladas", "Tamales", "Pozole", "Mole", "Chiles en nogada", "Pescado a la veracruzana", "Cochinita pibil", "Ceviche", "Chiles rellenos", "Tostadas", "Sopes", "Gorditas", "Chalupas", "Chilaquiles", "Huevos rancheros", "Migas", "Pancakes", "Waffles", "Hot cakes", "French toast", "Omelette", "Scrambled eggs", "Fried eggs", "Boiled eggs", "Poached eggs", "Eggs benedict", "Eggs florentine", "Eggs sardou", "Eggs norwegian", "Eggs mornay", "Eggs en cocotte", "Eggs a la bourguignonne", "Panqueques", "Wafles", "Hot cakes", "Tostadas francesas", "Omelette", "Huevos revueltos", "Huevos fritos", "Huevos cocidos", "Huevos escalfados", "Huevos benedictinos", "Huevos florentinos", "Huevos sardou", "Huevos noruegos", "Huevos mornay", "Huevos en cocotte", "Pasta alfredo", "Pasta carbonara", "Pasta bolognesa", "Pasta marinara", "Pasta arrabiata", "Pasta puttanesca", "Pasta primavera", "Pasta aglio e olio", "Pasta alla norma", "Pasta alla vodka", "Pasta alla papalina", "Pasta alla gricia", "Pasta alla amatriciana", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pasta alla gricia", "Pasta alla carbonara", "Pasta alla cacio e pepe", "Pasta alla matriciana", "Pizza de queso", "Pizza de pepperoni", "Pizza de hawaiana", "Pizza de jamón", "Pizza de salami", "Pizza de champiñones", "Pizza de pollo", "Pizza de carne", "Pizza de vegetales", "Pizza de cuatro quesos", "Pizza de margarita", "Pizza de albahaca", "Pizza de espinacas", "Pizza de alcachofas", "Pizza de aceitunas", "Pizza de anchoas", "Pizza de atún", "Pizza de camarones", "Pizza de cangrejo", "Pizza de langosta", "Pizza de mejillones", "Pizza de ostras", "Pizza de pulpo", "Pizza de salmón", "Pizza de trucha", "Pizza de cordero", "Pizza de pato", "Pizza de pavo", "Pizza de res", "Pizza de cerdo", "Pizza de ternera", "Pizza de búfalo", "Pizza de canguro", "Pizza de ciervo", "Pizza de jabalí", "Pizza de avestruz", "Pizza de cocodrilo", "Pizza de iguana", "Pizza de lagarto", "Pizza de serpiente", "Pizza de tortuga", "Pizza de rana", "Pizza de caracol", "Pizza de cangrejo", "Pizza de langosta", "Pizza de mejillones", "Pizza de ostras", "Pizza de pulpo", "Pizza de salmón", "Pizza de trucha", "Pizza de cordero", "Pizza de pato", "Pizza de pavo", "Pizza de res", "Pizza de cerdo", "Pizza de ternera", "Pizza de búfalo", "Pizza de canguro", "Pizza de ciervo", "Pizza de jabalí", "Pizza de avestruz", "Pizza de cocodrilo", "Pizza de iguana", "Pizza de lagarto", "Pizza de serpiente", "Pizza de tortuga", "Pizza de rana", "Pizza de caracol", "Pizza de cangrejo", "Pizza de langosta", "Pizza de mejillones", "Pizza de ostras", "Pizza de pulpo", "Pizza de salmón", "Pizza de trucha", "Pizza de cordero", "Pizza de pato"]
    # crear con las propiedades: name, description, avg_price, is_vegan, has_alcohol
    for dish in dishes:
        dish = {
            "name": dish,
            "description": "Plato de " + dish,
            "avg_price": random.randint(1, 200),
            "is_vegan": random.choice([True, False]),
            "has_alcohol": random.choice([True, False])
        }
        aura.create_dish(dish)
    
#relaciones entre ingredientes y platos
def fill_db_dish_ingredients():
    aura = AuraNeo4j()
    # obtener todos los ingredientes y platos
    ingredients = aura.get_all_ingredients()
    dishes = aura.get_all_dishes()
    # crear 1000 relaciones entre ingredientes y platos con datos random
    for _ in range(1500):
        relationship = {
            "dish_id": random.choice(dishes),
            "ingredient_id": random.choice(ingredients),
            "quantity": random.randint(1, 1000),
            "cook_method": random.choice(["fry", "boil", "bake", "grill", "steam", "saute", "roast", "poach"]),
            "cook_time": random.randint(1, 100)
        }
        aura.dish_has_ingredient(relationship)

def fill_db_restaurants():
    aura = AuraNeo4j()
    # crear 1000 restaurantes con datos random y los user_id deben ser unicos
    #array de restaurantes
    restaurants = ["Taco Bell", "McDonald's", "Burger King", "Wendy's", "KFC", "Pizza Hut", "Domino's", "Papa John's", "Little Caesars", "Subway", "Starbucks", "Dunkin'", "Tim Hortons", "Krispy Kreme", "Panera Bread", "Chipotle", "Taco Bell", "Qdoba", "Moe's", "Del Taco", "El Pollo Loco", "Popeyes", "Church's", "Raising Cane's", "Wingstop", "Buffalo Wild Wings", "Hooters", "Applebee's", "Chili's", "TGI Fridays", "Ruby Tuesday", "Olive Garden", "Red Lobster", "Outback", "Texas Roadhouse", "LongHorn", "Golden Corral", "Cracker Barrel", "Denny's", "IHOP", "Waffle House", "Perkins", "Bob Evans", "Shoney's", "Friendly's", "Johnny Rockets", "Fuddruckers", "Red Robin", "Five Guys", "In-N-Out", "Shake Shack", "Whataburger", "Jack in the Box", "Carl's Jr.", "Hardee's", "Sonic", "Dairy Queen", "Culver's", "Freddy's", "Checkers", "White Castle", "A&W", "Arby's", "Quiznos", "Firehouse Subs", "Jersey Mike's", "Jimmy John's", "Potbelly", "Schlotzsky's", "Jason's Deli", "McAlister's", "Einstein Bros", "Bruegger's", "Noah's", "Corner Bakery", "Au Bon Pain", "La Madeleine", "Zaxby's", "Bojangles", "Cook Out", "Captain D's", "Cicis", "Round Table", "Papa Murphy's", "CiCi's", "Peter Piper", "Godfather's", "Gatti's", "Mazzio's", "Pizza Inn", "Chuck E. Cheese's", "Peter Piper", "Godfather's", "Gatti's", "Mazzio's", "Pizza Inn", "Chuck E. Cheese's", "Peter Piper", "Godfather's", "Gatti's", "Mazzio", "Sonic"]
    for _ in range(1000):
        rand = random.randint(1, 1000)
        rand_hour = random.randint(1, 11)
        rand_price = random.randint(1, 200)
        rand_restaurant = random.choice(restaurants)
        restaurant = {
            # el user ID es el nombre del restaurante en minusculas y sin espacios+_rand+@gmail.com y en name el nombre del restaurante + rand
            "user_id": rand_restaurant.replace(" ", "").lower() + "_" + str(rand) + "@gmail.com",
            "name": rand_restaurant + " " + str(rand),
            "rating": random.randint(1, 5),
            "schedule": str(rand_hour) + ":00 - " + str(rand_hour + 12) + ":00",
            "password": "1234",
            "sells_alcohol": random.choice([True, False]),
            "petFriendly": random.choice([True, False]),
            "prices": str(rand_price) + " - " + str(rand_price + 100),
            "imagen": "https://www.tuexperto.com/wp-content/uploads/2022/06/restaurantes-generico.jpg",

        }
        aura.create_restaurant(restaurant)

# relaciones entre restaurantes y platillos
def fill_db_restaurant_dishes():
    aura = AuraNeo4j()
    # obtener todos los restaurantes y platos
    restaurants = aura.get_all_restaurants()
    dishes = aura.get_all_dishes()
    # crear 1000 relaciones entre restaurantes y platos con datos random
    rand_hour = random.randint(1, 11)
    for _ in range(1500):
        relationship = {
            "restaurant_id": random.choice(restaurants),
            "dish_id": random.choice(dishes),
            "price": random.randint(1, 200),
            "sell_time": str(rand_hour) + ":00 - " + str(rand_hour + 12) + ":00",
            "cost": random.randint(1, 150),
        }
        aura.restaurant_sells(relationship)

# relaciones entre restaurantes y locaciones
def fill_db_restaurant_locations():
    aura = AuraNeo4j()
    # obtener todos los restaurantes y locaciones
    restaurants = aura.get_all_restaurants()
    locations = aura.get_all_location_zones()
    # crear 1000 relaciones entre restaurantes y locaciones con datos random
    for _ in range(1500):
        relationship = {
            # con estas propiedades street: $street, avenue: $avenue, number: $number, community: $community, reference: $reference
            "restaurant_id": random.choice(restaurants),
            "zone": random.choice(locations),
            "street": "Calle " + str(random.randint(1, 100)),
            "avenue": "Avenida " + str(random.randint(1, 100)),
            "number": random.randint(1, 100),
            "community": "Comunidad " + str(random.randint(1, 100)),
            "reference": "Referencia " + str(random.randint(1, 100)),
        }
        aura.restaurant_located_in(relationship)

# crecion de parqueos
def fill_db_parkings():
    aura = AuraNeo4j()
    # crear 50 parqueos con datos random
    for i in range(50):
        parking = {
            # con estas propiedades: parking_id: $parking_id, price_per_hour: $price_per_hour, capacity: $capacity, handicap_friendly: $handicap_friendly, has_security: $has_security, is_covered: $is_covered
            "parking_id": "Parqueo " + str(i + 1),
            "price_per_hour": random.randint(0, 100),
            "capacity": random.randint(10, 100),
            "handicap_friendly": random.choice([True, False]),
            "has_security": random.choice([True, False]),
            "is_covered": random.choice([True, False])
        }
        aura.create_parking(parking)

# relaciones entre restaurantes y parqueos
def fill_db_restaurant_parkings():
    aura = AuraNeo4j()
    # obtener todos los restaurantes y parqueos
    restaurants = aura.get_all_restaurants()
    parkings = aura.get_all_parkings()
    # crear 100 relaciones entre restaurantes y parqueos con datos random
    for _ in range(2000):
        relationship = {
            # con estas propiedades vallet_parking: $vallet_parking, free_hours: $free_hours, exclusive: $exclusive
            "restaurant_id": random.choice(restaurants),
            "parking_id": random.choice(parkings),
            "vallet_parking": random.choice([True, False]),
            "free_hours": random.randint(0, 5),
            "exclusive": random.choice([True, False])
        }
        aura.restaurant_has_parking(relationship)

# relacion entre parqueos y locaciones
def fill_db_parking_locations():
    aura = AuraNeo4j()
    # obtener todos los parqueos y locaciones
    parkings = aura.get_all_parkings()
    locations = aura.get_all_location_zones()
    # crear 50 relaciones entre parqueos y locaciones con datos random
    for _ in range(70):
        relationship = {
            # con estas propiedades postal_code: $postal_code
            "parking_id": random.choice(parkings),
            "zone": random.choice(locations),
            "street": "Calle " + str(random.randint(1, 100)),
            "avenue": "Avenida " + str(random.randint(1, 100)),
            "number": random.randint(1, 100),
            "community": "Comunidad " + str(random.randint(1, 100)),
            "reference": "Referencia " + str(random.randint(1, 100)),
        }
        aura.parking_in(relationship)

# creacion de usuarios
def fill_db_users():
    aura = AuraNeo4j()
    # crear 1000 usuarios con datos random y los user_id deben ser unicos
    #array de usuarios
    name = ["Juan", "Pedro", "Maria", "Jose", "Luis", "Carlos", "Ana", "Rosa", "Elena", "Sofia", "Fernando", "Jorge", "Ricardo", "Roberto", "Miguel", "Raul", "Arturo", "Alejandro", "Javier", "Daniel", "Manuel", "Ramon", "Antonio", "Alberto", "Guillermo", "Hector", "Oscar", "Eduardo", "Francisco", "Ernesto", "Rafael", "Salvador", "Benjamin", "Cesar", "David", "Emilio", "Felipe", "Gustavo", "Ignacio", "Ismael", "Julio", "Leonardo", "Martin", "Nestor", "Pablo", "Quirino", "Rodrigo", "Santiago", "Tomas", "Uriel", "Victor", "Xavier", "Yahir", "Zacarias", "Abigail", "Beatriz", "Carmen", "Diana", "Eva", "Frida", "Gabriela", "Hilda", "Irene", "Juana", "Karla", "Leticia", "Mariana", "Nadia", "Olivia", "Patricia", "Rebeca", "Sara", "Teresa", "Ursula", "Veronica", "Wendy", "Ximena", "Yolanda", "Zulema", "Adrian", "Braulio", "Clemente", "Dante", "Ezequiel", "Fidel", "Gerardo", "Humberto", "Isaias", "Jacinto", "Lorenzo", "Marcos", "Nemesio", "Octavio", "Porfirio", "Quintin", "Rogelio", "Sergio", "Teodoro", "Ubaldo", "Vicente", "Walter", "Xicotencatl", "Yago", "Zacarias"]
    lastname = ["Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez", "Diaz", "Reyes", "Morales", "Jimenez", "Ortiz", "Castillo", "Ruiz", "Vargas", "Ramos", "Mendoza", "Cruz", "Aguilar", "Silva", "Mendez", "Salazar", "Chavez", "Guerrero", "Vasquez", "Soto", "Gutierrez", "Ortega", "Reyes", "Nunez", "Herrera", "Medina", "Aguirre", "Arias", "Barajas", "Bautista", "Becerra", "Beltran", "Bermudez", "Bernal", "Bravo", "Cabrera", "Calderon", "Campos", "Cardenas", "Carmona", "Carrillo", "Carranza", "Carrasco", "Carrillo", "Castañeda", "Cervantes", "Chavez", "Contreras", "Cordero", "Corona", "Coronado", "Cortes", "Covarrubias", "Cruz", "De la Cruz", "De la Rosa", "De Leon", "Delgado", "Diaz", "Dominguez", "Duarte", "Estrada", "Fernandez", "Figueroa", "Flores", "Fuentes", "Galindo", "Gallegos", "Garcia", "Garza", "Gaspar", "Gaytan", "Gil", "Gomez", "Gonzalez", "Guerrero"]

    for i in range(1500):
       # con estas propiedades: user_id: $user_id, password: $password, name: $name, lastname: $lastname, brithdate: $birthdate, spending: $spending, "has_car: $has_car, image: $image
        rand_name = random.choice(name)
        rand_lastname = random.choice(lastname)
        user = {
            "user_id": rand_name.lower() + rand_lastname.lower() + str(i) + "@gmail.com",
            "password": "1234",
            "name": rand_name,
            "lastname": rand_lastname,
            # fecha de nacimiento random AAAA-MM-DD.
            "birthdate": str(random.randint(1950, 2005)) + "-" + str(random.randint(10, 12)) + "-" + str(random.randint(1, 28)),
            "spending": random.randint(10, 1000),
            "has_car": random.choice([True, False]),
            "image": random.choice(["https://preview.redd.it/created-random-people-using-chatgpt-midjourney-do-you-know-v0-q1aa450i5dqb1.png?width=1024&format=png&auto=webp&s=c4e9abc47d193474a2fa1a7e337d9d9340dce947", "https://www.google.com/url?sa=i&url=https%3A%2F%2Fsoundcloud.com%2Fdoruk-durukan%2Fnice-song&psig=AOvVaw3HyYDjRhm1HL1BzTqni7FT&ust=1713427719002000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNCO_OblyIUDFQAAAAAdAAAAABAT", "https://yt3.googleusercontent.com/2p3yM-QcYgMu0WGWgWMgsIBDjeXrOmd2T1At3LN0VpoNiXrnHgNI_8jFhp2qXE9RW8q09AyI=s900-c-k-c0x00ffffff-no-rj", "https://www.google.com/url?sa=i&url=https%3A%2F%2Ftwitter.com%2Fhansgetzeflamm2&psig=AOvVaw3HyYDjRhm1HL1BzTqni7FT&ust=1713427719002000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNCO_OblyIUDFQAAAAAdAAAAABA7"]),   
              
        }
        aura.create_diner(user)

# relaciones entre usuarios y restaurantes visited
def fill_db_diner_restaurants_visit():
    aura = AuraNeo4j()
    # obtener todos los usuarios y restaurantes
    diners = aura.get_all_diners()
    restaurants = aura.get_all_restaurants()
    # crear 1000 relaciones entre usuarios y restaurantes con datos random
    for _ in range(1500):
        rand_restaurant = random.choice(restaurants)
        dishes = aura.search_sells_relationship(rand_restaurant)
        # tomar solo el nombre de los platos
        dishes = [dish["name"] for dish in dishes]
        if not dishes:
            continue
        relationship = {
            # con estas propiedades dishes: $dishes, total: $total, date: $date, rating: $rating, comment: $comment
            "user_id": random.choice(diners),
            "restaurant_id": rand_restaurant,
            #lista de platos
            "dishes": [random.choice(dishes) for _ in range(1)],
            "total": random.randint(10, 1000),
            # fecha datetime now formato: 2024-04-16T06:17:40.397000000Z
            "date": str(datetime),
            "rating": random.randint(1, 5),
            "comment": "Comentario " + str(random.randint(1, 100))            

        }
        aura.create_visit(relationship)

# relaciones entre usuarios y restaurantes diners_on_restaurant
def fill_db_diner_on_restaurants():
    aura = AuraNeo4j()
    # obtener todos los usuarios y restaurantes
    diners = aura.get_all_diners()
    restaurants = aura.get_all_restaurants()
    # crear 1000 relaciones entre usuarios y restaurantes con datos random
    for _ in range(1500):
        relationship = {
            # con estas propiedades its_fav: $its_fav, user_likes: $user_likes, comments: $comments
            "diner_id": random.choice(diners),
            "restaurant_id": random.choice(restaurants),
            "its_fav": random.choice([True, False]),
            "user_likes": random.choice([True, False]),
            "comments": "Comentario " + str(random.randint(1, 100))
        }
        aura.diner_on_restaurant(relationship)

# relaciones entre usuarios y platillos dish_opinion
def fill_db_diner_dish_opinion():
    aura = AuraNeo4j()
    # obtener todos los usuarios y platos
    diners = aura.get_all_diners()
    dishes = aura.get_all_dishes()
    # crear 1000 relaciones entre usuarios y platos con datos random
    for _ in range(1500):
        relationship = {
            # con estas propiedades favorite: $favorite, likes: $likes, comment: $comment
            "diner_id": random.choice(diners),
            "dish_id": random.choice(dishes),
            "favorite": random.choice([True, False]),
            "likes": random.choice([True, False]),
            "comment": "Comentario " + str(random.randint(1, 100))
        }
        aura.diner_opinion(relationship)

# relaciuon entre restaurante y locacion HAS_DELIVERY
def fill_db_restaurant_has_delivery():
    aura = AuraNeo4j()
    # obtener todos los restaurantes y locaciones
    restaurants = aura.get_all_restaurants()
    locations = aura.get_all_location_zones()
    # crear 1000 relaciones entre restaurantes y locaciones con datos random
    for _ in range(500):
        relationship = {
            # con estas propiedades {price: $price, time: $time, own_delivery: $own_delivery}
            "restaurant_id": random.choice(restaurants),
            "zone": random.choice(locations),
            "price": random.randint(0, 100),
            "time": str(random.randint(1, 90)) + " min",
            "own_delivery": random.choice([True, False])
        }
        aura.restaurant_has_delivery(relationship)



if __name__ == "__main__":
    fill_db_ingredients()    
    #fill_db_dishes()
    #fill_db_dish_ingredients()
    #fill_db_restaurants()
    #fill_db_restaurant_dishes()
    #fill_db_restaurant_locations()
    #fill_db_parkings()
    #fill_db_restaurant_parkings()
    #fill_db_parking_locations()
    #fill_db_users()
    #sistema_recomendacion("cas21700@uvg.edu.gt")
    #fill_db_diner_restaurants()
    #fill_db_diner_on_restaurants()
    #fill_db_diner_dish_opinion()
    #fill_db_restaurant_has_delivery()
    #print("hello world")
    aura = AuraNeo4j()
    aura.load_ingredients_from_csv("./backend/csv/ingredientes.csv")
    aura.load_dishes_from_csv("./backend/csv/dishes.csv")
    aura.load_parking_from_csv("./backend/csv/parkings.csv")
    