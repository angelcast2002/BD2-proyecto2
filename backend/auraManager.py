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
