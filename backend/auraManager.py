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

    def create_comensal(self, user: dict):
        with self.driver.session() as session:
            return session.write_transaction(self._create_comensal, user)

    @staticmethod
    def _create_comensal(tx: Transaction, user: dict):
        query = (
            "CREATE (c:Comensal {userid: $userid, password: $password, nombre: $nombre, "
            "apellido: $apellido, edad: $edad, presupuesto_prom: $presupuesto_prom, "
            "tieneVehiculo: $tieneVehiculo, fecha_registro: $fecha_registro, imagen: $imagen}) "
            "RETURN c"
        )
        return tx.run(query, **user).single()[0]
