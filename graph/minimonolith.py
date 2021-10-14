'''
This is a sketch module of the basic functionality to creat a keyword in context graph in Neo4J locally.

2021.10.13

'''

import os
import json
from git import Repo
from neo4j import GraphDatabase
import mdparser as MDP

ROOTFOLDER = r"C:\git\mb\KWIC\graph\clone"


def create_cipher(in_dict):
    '''Takes a dictionary and returns a set of cipher friendly attributes.'''
    keys = list(in_dict.keys())
    roll_cipher = "{ "
    size = len(keys)
    for indx, i in enumerate(keys):
        slug = '{} : "{}"'.format(i, in_dict[i])
        if indx == size-1:
            roll_cipher += slug + " }"
        else:
            roll_cipher += slug + ", "
    roll_cipher = roll_cipher.replace("ms.", "ms")
    roll_cipher = roll_cipher.replace("\\", "\\\\")
    return roll_cipher


def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout


def get_files(inpath, extension="md"):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(inpath):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == extension:
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist


def get_repo(git_url):
    try:
        Repo.clone_from(git_url,ROOTFOLDER )
    except:
        print("Files have bene grabbed.")


def create_node(tx, type, map):
    tx.run('CREATE (n: {}) SET n = {}'.format(type, map))


def create_edge(tx, type1, node1, edge, type2, node2):
    session.write_transaction(create_node, type1, node1)
    session.write_transaction(create_node, type2, node2)
    cypher = '''MATCH (a:{} {{name: "node1"}})
MATCH (b:{} {{name: "node2"}})
MERGE (a)-[r:{}]->(b)
    '''.format(type1, type2, edge)
    print(cypher)
    tx.run(cypher)

# logic

#simulate json payload input
config_file = open("config.json")
config_str = config_file.read()
config = json.loads(config_str)

get_repo(config["gitrepo"])
list_of_files = get_files(ROOTFOLDER, "md")

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=(config["neo_user"], config["neo_pass"]))

map = "{ name: '"+config["docset"]+"'}"
with driver.session() as session:
    session.write_transaction(create_node, "docset", map)

for f in list_of_files:
    try:
        mdparser = MDP.MDParser()
        text_as_lines = mdparser.get_raw_body(f).split("\n")
        metadata = mdparser.process_meta()
        metadata["path"] = f
        path = f.replace("\\", "\\\\")
        map = create_cipher(metadata)
        print(map)

        with driver.session() as session:
            session.write_transaction(create_node, "article", map)
        # with driver.session() as session:
        #     session.write_transaction(create_edge, "docset", "azure-stack-docs", "CONTAINS", "article", path)
    except:
        print("Error: {}".format(f))


# for indx, i in enumerate(text_as_lines):
#     line_no = indx+1
#     print("{} : {}".format(line_no, i))



# map = "{ name: 'doc-set', item: 'test item 2' }"

# with driver.session() as session:
#     session.write_transaction(create_node, map)

driver.close()