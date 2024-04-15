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
            "MERGE (c:Diner {user_id: $user_id, password: $password, name: $name, "
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
            "MERGE (c:Restaurant {user_id: $user_id, password: $password, name: $name, "
            "prices: $prices, rating: $rating, schedule: $schedule, "
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
        search_query = "MATCH (i:Ingredient {name: $name, type: $type}) RETURN i"
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
            "MERGE (p:Parking {parking_id: $parking_id}) "
            "RETURN p"
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
        create_query = (
            "MATCH (u:Diner {user_id: $user_id}), (c:Restaurant {user_id: $restaurant_id}) "
            "CREATE (u)-[r:VISITED {dishes: $dishes, total: $total, date: $date, rating: $rating, comment: $comment}]->(c) "
            "RETURN r"
        )
        try:
            return tx.run(create_query, **visit).single()[0]
        except Exception as e:
            return 400
    # buscar la relacion entre restaurante y plato llamada sells con propiedades: price, sell_time and cost. si existe, retornar
    # la lista de platos que vende el restaurante

    def search_sells_relationship(self, restaurant_id: str):
        with self.driver.session() as session:
            return session.read_transaction(self._search_sells_relationship, restaurant_id)

    @staticmethod
    def _search_sells_relationship(tx: Transaction, restaurant_id: str):
        search_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id})-[s:SELLS]->(d:Dish) "
            "RETURN d.name AS dish_name"
        )
        try:
            result = tx.run(search_query, restaurant_id=restaurant_id)
            return [record["dish_name"] for record in result]
        except Exception as e:
            return None

    
    
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

        search_query = (
            "MATCH (d:Diner {user_id: $diner_id}), (r:Restaurant {user_id: $restaurant_id}) "
            "MERGE (d)-[dor:DINER_ON_RESTAURANT {its_fav: $its_fav, user_likes: $user_likes, comments: $comments}]->(r) "
            "RETURN dor"
        )

        try:
            return tx.run(search_query, **diner_on_restaurnt).single()[0]
        except Exception as e:
            return 400


    # Crear relacion entre restaurante y plato llamada sells con propiedades: price, sell_time and cost
    def restaurant_sells(self, relationship: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._restaurant_sells, relationship)
        
    @staticmethod
    def _restaurant_sells(tx: Transaction, relationship: dict):
        search_query = (
            "MATCH (r:Restaurant {user_id: $restaurant_id}), (d:Dish {name: $dish_name}) "
            "CREATE (r)-[s:SELLS {price: $price, sell_time: $sell_time, cost: $cost}]->(d) "
            "RETURN s"
        )
        try:
            return tx.run(search_query, **relationship).single()[0]
        except Exception as e:
            return 400
