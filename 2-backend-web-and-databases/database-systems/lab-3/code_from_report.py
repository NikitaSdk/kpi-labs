# Code extracted from the lab report (report.pdf)

import neo4j
import random

#Підключення до бази даних Neo4j
driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "<password>"))
with driver.session() as session:
    #Очищення минулих даних
    session.run("MATCH (n) DETACH DELETE n")
    # Створення семи вузлів типу 1
    for i in range(7):
        session.run("CREATE (n:Node1 {id: $id})", {"id": i + 1})
    # Створення п'яти вузлів типу 2
    for i in range(5):
        session.run("CREATE (n:Node2 {id: $id})", {"id": i + 1})
    # Створення зв'язків між вузлами
    for i in range(7):
        randnode2 = random.randint(1,5)
        session.run("MATCH (n1:Node1 {id: $id1}), (n2:Node2 {id: $id2}) CREATE (n1)-[:CONNECTION]->(n2)",{"id1": i + 1, "id2": randnode2})
    for j in range(5):
        randnode1 = random.randint(1,7)
        session.run("MATCH (n1:Node1 {id: $id1}), (n2:Node2 {id: $id2}) CREATE (n2)-[:CONNECTION]->(n1)", {"id1": randnode1, "id2": j + 1})
driver.close()
