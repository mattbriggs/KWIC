'''
This is a sketch module of the basic functionality to creat a keyword in context graph in Neo4J locally.

2021.10.13

'''

import os
import json
import uuid
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

def clear_line(instring):
    '''Clear problem characters'''
    instring = instring.replace("\\", "\\\\")
    instring = instring.replace("\"", "\\\"")
    instring = instring.replace("\'", "\\\'")
    return instring

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


def create_edge(tx, source, edge, target):
    '''Send the source node to the target node:
    a:type {name: "unique1"), b:type {name: "unique2"), (a) -[r:EDGE]-> (b)
    Each node:
    node type
    ID attribitue (such as name)
    Unique name.
    '''
    cypher = '''MATCH (a:{} {{{}: "{}"}})
MATCH (b:{} {{{}: "{}"}})
MERGE (a)-[r:{}]->(b)
    '''.format(source[0], source[1], source[2], target[0], target[1], target[2], edge)
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
        
        source = ["article", "path", path]
        target = ["docset", "name", config["docset"]] 
        with driver.session() as session:
            session.write_transaction(create_edge, source, "CONTAINS", target)
        

        for indx, i in enumerate(text_as_lines):
            line_text = clear_line(i)
            line_no = indx+1
            line_id = str(uuid.uuid4())
            line_map = "{ lineid : '" + line_id + "', "
            line_map += "lineno: '" + str(line_no) + "', "
            line_map += "text: '" + line_text + "' }"
            print(line_map)
            with driver.session() as session:
                session.write_transaction(create_node, "line", line_map)
            driver.close()
            source_line = ["line", "lineid", line_id]
            target_doc = ["article", "path", path]
            with driver.session() as session:
                session.write_transaction(create_edge, source_line, "BODY", target_doc)
            

    except:
        print("*** Error: {}".format(f))

driver.close()