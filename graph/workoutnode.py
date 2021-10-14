from neo4j import GraphDatabase
import json

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "reb00REB"))

# def create_friend_of(tx, name, friend):
#     tx.run("MATCH (a:Person) WHERE a.name = $name "
#            "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
#            name=name, friend=friend)

def create_edge(tx, type1, node1, edge, type2, node2):
    session.write_transaction(create_node, type1, node1)
    session.write_transaction(create_node, type2, node2)
    cypher = '''MATCH (a:{} {{name: "node1"}})
MATCH (b:{} {{name: "node2"}})
MERGE (a)-[r:{}]->(b)
    '''.format(type1, type2, edge)
    print(cypher)
    tx.run(cypher)

def create_node(tx, type, map):
    tx.run('CREATE (n: {}) SET n = {}'.format(type, map))

# with driver.session() as session:
#     session.write_transaction(create_friend_of, "Alice", "Bob")

# with driver.session() as session:
#     session.write_transaction(create_friend_of, "Alice", "Carl")

# This works::
# map = "{ name: 'doc-set', item: 'test item 2' }"

# with driver.session() as session:
#     session.write_transaction(create_node, "test", map)

type1 = "test"
node1 = '{ name: "node1", detail: "This is the first node." }'
type2 = "test"
node2 = '{ name: "node2", detail: "This is the second node." }'

with driver.session() as session:
    session.write_transaction(create_edge, type1, node1, "TESTB", type2, node2)

driver.close()

